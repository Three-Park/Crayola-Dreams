from django.shortcuts import render, get_object_or_404
from .models import Diary, Comment
from .apps import CommentConfig
import torch

def generate(input_text): 
    U_TKN = '<usr>'
    S_TKN = '<sys>'
    EOS = '</s>'
    SENT = '<unused1>'
    
    koGPT2_TOKENIZER = CommentConfig.koGPT2_TOKENIZER
    model = CommentConfig.model
    
    q = input_text
    generated_comment = ""
    sent = ""
    while True:
        device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        input_ids = torch.LongTensor(koGPT2_TOKENIZER.encode(U_TKN + q + SENT + sent + S_TKN + generated_comment)).unsqueeze(dim=0)
        input_ids=input_ids.to(device)
        pred = model(input_ids)
        pred = pred.logits
        gen = koGPT2_TOKENIZER.convert_ids_to_tokens(torch.argmax(pred, dim=-1).squeeze().tolist())[-1]
        if gen == EOS:
            break
        generated_comment += gen.replace("▁", " ")
    return generated_comment

def gen_comment(request, diary_id):
    diary = get_object_or_404(Diary, pk=diary_id)
    descriptions = generate(diary.content)
    comment = Comment.objects.create(diary=diary, description=descriptions)
    comment.save()

    return render(request, 'view_comment.html', {'descriptions': descriptions})
