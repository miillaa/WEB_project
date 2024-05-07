def emotion_html():
    with open('emotions.txt') as f:
        emotions_list = list(map(lambda x: x.strip(), f.readlines()))
    selection_buttons = []
    for i in range(len(emotions_list)):
        selection_buttons.append(f'''
                                <div class="form-group form-check">
                                    <input type="checkbox" class="form-check-input" id="{emotions_list[i]}Checkbox" name="emotion{i}" value="{emotions_list[i]}">
                                    <label class="form-check-label" for="{emotions_list[i]}Checkbox">{emotions_list[i]}</label>
                                </div>''')
    return f'''<!DOCTYPE html>
                <html lang="en">
                <head>
                    <meta charset="UTF-8">
                    <meta name="viewport" content="width=device-width, initial-scale=1.0">
                    <title>Emotion Buttons</title>
                </head>
                <body>
                    <div>
                        <form class="login_form" method="post">

                            <div class="form-group">{'\n'.join(selection_buttons)}           
                            </div>

                            <button type="submit" class="btn btn-primary">Записаться</button>
                        </form>
                    </div>
                </body>
                </html>'''
