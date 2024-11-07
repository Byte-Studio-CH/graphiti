"""
Copyright 2024, Zep Software, Inc.

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from typing import Iterable, List

from openai import AsyncOpenAI, AsyncAzureOpenAI
from openai.types import EmbeddingModel

from .client import EmbedderClient, EmbedderConfig

# DEFAULT_EMBEDDING_MODEL = 'text-embedding-3-small'
DEFAULT_EMBEDDING_MODEL = 'text-embedding-3-large'


class OpenAIEmbedderConfig(EmbedderConfig):
    embedding_model: EmbeddingModel | str = DEFAULT_EMBEDDING_MODEL
    api_key: str | None = None
    base_url: str | None = None
    use_azure: bool | None = False


class OpenAIEmbedder(EmbedderClient):
    """
    OpenAI Embedder Client
    """

    def __init__(self, config: OpenAIEmbedderConfig | None = None):
        if config is None:
            config = OpenAIEmbedderConfig()
        self.config = config
        if config.use_azure:
            self.client = AsyncAzureOpenAI(api_key=config.api_key, azure_endpoint=config.base_url,  api_version="2024-07-01-preview",)
        else:
            self.client = AsyncOpenAI(api_key=config.api_key, base_url=config.base_url)

    async def create(
        self, input_data: str | List[str] | Iterable[int] | Iterable[Iterable[int]]
    ) -> list[float]:
        result = await self.client.embeddings.create(
            input=input_data, model=self.config.embedding_model
        )
        return result.data[0].embedding[: self.config.embedding_dim]
