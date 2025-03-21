from typing import AsyncGenerator, TypeVar, Callable, List, Generic, Any

T = TypeVar('T')
U = TypeVar('U')
V = TypeVar('V')

class Pipeline:
    """
    A flexible pipeline that chains multiple async generators.

    Each step is a function that takes an async generator and returns a new async generator.
    """

    def __init__(self, source: AsyncGenerator[Any, None]):
        """Initialize the pipeline with a source async generator."""
        self.source = source
        self.steps: List[Callable[[AsyncGenerator[Any, None]], AsyncGenerator[Any, None]]] = []

    def add_step(self, transform: Callable[[AsyncGenerator[Any, None]], AsyncGenerator[Any, None]]):
        """
        Add a transformation step to the pipeline.

        Args:
            transform: A function that takes an async generator and returns an async generator

        Returns:
            The pipeline instance for method chaining
        """
        self.steps.append(transform)
        return self

    def __aiter__(self):
        """Make the pipeline itself an async generator."""
        return self._execute()

    async def _execute(self):
        """
        Execute the pipeline by chaining all generators together.

        Yields:
            Values from the final step of the pipeline
        """
        current_gen = self.source

        # Apply each transformation step
        for step in self.steps:
            current_gen = step(current_gen)

        # Yield all items from the final generator
        async for item in current_gen:
            yield item

    async def collect(self):
        """
        Collect all results from the pipeline into a list.

        Returns:
            A list containing all output items from the pipeline
        """
        results = []
        async for item in self:
            results.append(item)
        return results