"""Base agent class for ADK-based interview agents."""
from abc import ABC, abstractmethod
from typing import Any, Dict, Optional, List
from pydantic import BaseModel, Field
from google.genai import Client
import config


class AgentMemory(BaseModel):
    """Memory structure for agents."""
    short_term: List[Dict[str, Any]] = Field(default_factory=list)
    long_term: Dict[str, Any] = Field(default_factory=dict)
    working_memory: Dict[str, Any] = Field(default_factory=dict)


class AgentConfig(BaseModel):
    """Configuration for an agent."""
    name: str
    role: str
    temperature: float = 0.7
    response_format: str = "text"  # "text" or "json"
    max_iterations: int = 1
    tools: List[str] = Field(default_factory=list)


class BaseInterviewAgent(ABC):
    """Base class for all interview agents using ADK patterns."""
    
    def __init__(
        self,
        client: Client,
        config: AgentConfig,
        system_prompt: str,
    ):
        """Initialize the agent.
        
        Args:
            client: Google GenAI client
            config: Agent configuration
            system_prompt: System instruction for the agent
        """
        self.client = client
        self.config = config
        self.system_prompt = system_prompt
        self.memory = AgentMemory()
        self._tools = {}
    
    def register_tool(self, name: str, tool_func: callable, description: str):
        """Register a tool that this agent can use.
        
        Args:
            name: Tool name
            tool_func: Callable tool function
            description: Tool description
        """
        self._tools[name] = {
            "function": tool_func,
            "description": description,
        }
    
    def update_memory(self, key: str, value: Any, memory_type: str = "working"):
        """Update agent memory.
        
        Args:
            key: Memory key
            value: Memory value
            memory_type: Type of memory ("short_term", "long_term", "working")
        """
        if memory_type == "short_term":
            self.memory.short_term.append({key: value})
        elif memory_type == "long_term":
            self.memory.long_term[key] = value
        else:
            self.memory.working_memory[key] = value
    
    def get_memory(self, key: str, memory_type: str = "working") -> Optional[Any]:
        """Retrieve from agent memory.
        
        Args:
            key: Memory key
            memory_type: Type of memory to retrieve from
            
        Returns:
            Memory value or None
        """
        if memory_type == "working":
            return self.memory.working_memory.get(key)
        elif memory_type == "long_term":
            return self.memory.long_term.get(key)
        return None
    
    def clear_working_memory(self):
        """Clear working memory."""
        self.memory.working_memory = {}
    
    @abstractmethod
    def process(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Process input and generate output.
        
        Args:
            context: Input context for the agent
            
        Returns:
            Agent output
        """
        pass
    
    def _generate_response(
        self,
        user_message: str,
        temperature: Optional[float] = None,
        response_format: Optional[str] = None,
    ) -> str:
        """Generate a response using the LLM.
        
        Args:
            user_message: User message to process
            temperature: Override default temperature
            response_format: Override default response format
            
        Returns:
            Generated response text
        """
        temp = temperature if temperature is not None else self.config.temperature
        fmt = response_format if response_format is not None else self.config.response_format
        
        gen_config = {
            "system_instruction": self.system_prompt,
            "temperature": temp,
        }
        
        if fmt == "json":
            gen_config["response_mime_type"] = "application/json"
        
        response = self.client.models.generate_content(
            model=config.MODEL,
            contents=user_message,
            config=gen_config,
        )
        
        return response.text
    
    def reflect(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Reflect on past actions and outcomes.
        
        This enables agents to learn from their interactions.
        
        Args:
            context: Context for reflection
            
        Returns:
            Reflection insights
        """
        reflection_prompt = f"""
Reflect on your recent actions and outcomes:

Context: {context}

Recent Memory: {self.memory.short_term[-5:] if self.memory.short_term else []}

Provide insights on:
1. What worked well
2. What could be improved
3. Patterns you notice
4. Adjustments for next time
"""
        
        reflection = self._generate_response(reflection_prompt, temperature=0.5)
        self.update_memory("last_reflection", reflection, "long_term")
        
        return {"reflection": reflection}
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(name={self.config.name}, role={self.config.role})"
