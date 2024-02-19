# current confirmation prompt
# def get_prompt():

#     content = f""" Analyse the image, provide its breif description by focusing on minor details as well in 3-8 words only.
#         """


#     return content
def get_prompt():

    content = f""" Analyse the image, 
    > if its a cloth then provide its breif description by focusing on minor details as well of the cloth, Ignore the surrounding items.
    > if its something else then focus on the major centered thing. forget other details.

    Don't Mention useless things like "Used machine", "Machine with reflection". Here "Used" and "reflection" are useless. 
    Just mention the product with its details like black washing machine etc.

    MAKE SURE TO RESPONSE IN UP TO 1-7 WORDS words only. 
        """

    return content


# def get_prompt():

#     content=  f""" Analyse the image and gather its provide its details in below format.
#             {{Season}} {{Weight/Type}} {{Feature/Style}} {{Style/Type}} {{Material/Filling}} {{Garment Type}} {{Gender}}

#             - Season (Winter, Summer, Spring, Autumn)
#             - Weight/Type (Ultralight, Lightweight, Mediumweight, Heavyweight)
#             - Garment Type (Coat, Jacket, Blazer, Parka, Trench, Vest)
#             - Feature/Style (Hooded, Collared, Zip-up, Button-up, Belted, Open Front)
#             - Style/Type (Puffer, Bubble, Bomber, Quilted, Fleece, Windbreaker, Peacoat)
#             - Material/Filling (Duck-Down, Goose Down, Synthetic, Wool, Cotton, Polyester, Leather)
#             - Gender (Mens, Womens, Unisex, Kids)

#             For example:
#             - Winter Ultralight Coat Hooded Puffer Jacket Bubble Coat Duck-Down Jacket Mens

#         """

#     return content
