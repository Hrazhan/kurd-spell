import gradio as gr
from difflib import Differ
from transformers import pipeline

model_id = "razhan/bart-kurd-spell-base"
# spell_corrector = pipeline("text2text-generation", model=model_id, return_all_scores=True)
spell_corrector = pipeline("text2text-generation", model=model_id, max_length=1024)



def correct_spell(text):
    d = Differ()
    if text is None:
        text = ""
    corrected = spell_corrector(text)[0]['generated_text']

    return [
        (token[2:], token[0] if token[0] != " " else None)
        for token in d.compare(text, corrected)
    ], corrected



demo = gr.Interface(
    correct_spell,
    [
        gr.Textbox(
            label="Input text",
            info="Initial text to be corrected",
            lines=3,
            value="نوووسینێکی ڕااست  بێهەڵە",
            rtl=True
        ),
    ],
    outputs=[
        gr.HighlightedText(
            label="Diff",
            combine_adjacent=True,
            show_legend=True,
            color_map={"-": "pink", "+": "green"},
            rtl=True,
            # container=True,
            elem_id="kurdi"
        ),
        gr.Textbox(label="Corrected Text", rtl=True, container=True)
    ],
    examples=[
        "حکومەتلە گفتوگۆحانی پەرلەماندا لەسەربودجەی نوێ ڕایگەیاند کە لە دەنگدانلەسەر بودجە بەردەوام دەبێت",
        "ژنەڤ کاندغدێکی کورد نەشتەرگەری بۆکەا",
        "فەستبخەرکرانی سێ هاووڵاتی لە شاری بۆکانلە لاین هێزە ئەمنییکەانەوە",
        "ئەم وێنجانەی وخارەوەش چەند ێونەیەکی دەزپێرکاوی مۆبایلەکەن",
        "خۆگزە توانیبام ژیان لە دیداری یەکەی ژاچگرێ بدەم",
        "هەرفەرمانبەرێک بەناشچایستە پلەی نوەزیفیوەرگرتبێتلێیدەسەرنێتەەو",
        "ماوەیەکەدەست ەب ئاامدەکسری کرا٦وە بۆ بەڕێوەچوونی ەششەمین فیستیڤاڵینێودەوڵەتیی هەولێرب ۆ شانۆ",
        "ەڵم ئارەزوومە کە فیلمێک لە سەرحۆریەکانی ێجەریای نێوچیڕۆکەکانیشەوان عەرەبیەوە بەرخهەم بهێنم",
        "پارەی ئەلکتترۆنیکی هیان راوی دیجیتاڵ جۆرە راوێکە کە تەنیا بە شێوەی ئەلیکترۆنیکی لەبەردەستەایە"
    

    ],
    title="Central Kurdish Neurl Spell Correction",
    # description="This is made as a fun side project, it's not to be relied on for production.",
    css="""
    #kurdi {
        text-align: right;
    }
    """,
    theme=gr.themes.Base(
        primary_hue="pink",
        secondary_hue="stone",
        text_size=gr.themes.sizes.text_lg,
        spacing_size=gr.themes.sizes.spacing_lg,
        radius_size=gr.themes.sizes.radius_lg,
        font=gr.themes.GoogleFont("Noto Sans"),

    ),
    allow_flagging='auto'
)
if __name__ == "__main__":
    demo.launch()