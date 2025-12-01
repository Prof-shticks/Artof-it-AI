from llama_cpp import Llama
import logging
from typing import Dict, List, Optional
import json


class LLaMAManager:
    def __init__(self, model_path: str, **kwargs):
        self.model_path = model_path
        self.logger = self._setup_logging()

        default_params = {
            'n_ctx': 4096,
            'n_threads': 8,
            'n_gpu_layers': 35,
            'verbose': False
        }
        default_params.update(kwargs)

        self.logger.info(f"Загрузка модели: {model_path}")
        try:
            self.llm = Llama(model_path=model_path, **default_params)
            self.logger.info("Модель успешно загружена!")
        except Exception as e:
            self.logger.error(f"Ошибка загрузки модели: {e}")
            raise

    def _setup_logging(self):
        logger = logging.getLogger(__name__)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            )
            handler.setFormatter(formatter)
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
        return logger

    def generate_response(self,
                          prompt: str,
                          max_tokens: int = 256,
                          temperature: float = 0.7,
                          top_p: float = 0.95,
                          **kwargs) -> Dict:
        try:
            output = self.llm(
                prompt,
                max_tokens=max_tokens,
                temperature=temperature,
                top_p=top_p,
                **kwargs
            )

            return {
                'text': output['choices'][0]['text'].strip(),
                'tokens_used': output['usage']['total_tokens'],
                'success': True
            }

        except Exception as e:
            self.logger.error(f"Ошибка генерации: {e}")
            return {
                'text': '',
                'tokens_used': 0,
                'success': False,
                'error': str(e)
            }

    def chat(self,
             message: str,
             system_prompt: str = "Ты полезный AI ассистент",
             **kwargs) -> str:
        formatted_prompt = f"""### System:
{system_prompt}

### Instruction:
{message}

### Response:"""

        result = self.generate_response(formatted_prompt, **kwargs)
        return result['text'] if result['success'] else "Ошибка генерации"

    def batch_process(self, prompts: List[str], **kwargs) -> List[Dict]:
        results = []
        for prompt in prompts:
            result = self.generate_response(prompt, **kwargs)
            results.append(result)
        return results

    def get_model_info(self) -> Dict:
        return {
            'model_path': self.model_path,
            'context_size': self.llm.context_params.n_ctx,
            'model_size': f"{self.llm.model_params.model_size / 1024 ** 3:.2f} GB"
        }