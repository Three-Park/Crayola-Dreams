from django.apps import AppConfig
import torch
from transformers import PreTrainedTokenizerFast

class CommentConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'comment'
    
    
    U_TKN = '<usr>'
    S_TKN = '<sys>'
    BOS = '</s>'
    EOS = '</s>'
    MASK = '<unused0>'
    SENT = '<unused1>'
    PAD = '<pad>'
        
    TOKENIZER = PreTrainedTokenizerFast.from_pretrained(
            "skt/kogpt2-base-v2",
            bos_token=BOS, eos_token=EOS, unk_token='<unk>',
            pad_token=PAD, mask_token=MASK
    )
    model = torch.load('Kogpt2_epoch5.pth', map_location=torch.device('cpu'))

