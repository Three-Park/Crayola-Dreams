from django.apps import AppConfig
import torch
from transformers import PreTrainedTokenizerFast


class CommentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comment'

    def ready(self):
        self.load_model()

    def load_model(self):
        U_TKN = '<usr>'
        S_TKN = '<sys>'
        BOS = '</s>'
        EOS = '</s>'
        MASK = '<unused0>'
        SENT = '<unused1>'
        PAD = '<pad>'

        self.koGPT2_TOKENIZER = PreTrainedTokenizerFast.from_pretrained(
            "skt/kogpt2-base-v2",
            bos_token=BOS, eos_token=EOS, unk_token='<unk>',
            pad_token=PAD, mask_token=MASK
        )

        self.model = torch.load('path_to_your_pretrained_model.pth', map_location=torch.device('cpu'))
