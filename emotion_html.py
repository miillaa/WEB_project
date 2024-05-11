def emotion_html():
    with open('emotions.txt', encoding='utf-8') as f:
        emotions_list = list(map(lambda x: x.strip(), f.readlines()))

    selection_buttons = []

    for i in range(len(emotions_list)):
        selection_buttons.append(f'''
            <div class="form-group form-check">
                <input type="checkbox" class="form-check-input" id="{emotions_list[i]}Checkbox" name="emotion{i}" value="{emotions_list[i]}">
                <label class="form-check-label" for="{emotions_list[i]}Checkbox">{emotions_list[i]}</label>
            </div>
        ''')

    return f'''
        <!DOCTYPE html>
        <html lang="en">
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Emotion Buttons</title>
            <style>
                body {{
                    font-family: Arial, sans-serif;
                    background-color: #f8f9fa;
                    margin: 0;
                    padding: 20px;
                }}
                .selection_form {{
                    max-width: 600px;
                    margin: auto;
                    padding: 20px;
                    border: 1px solid #ddd;
                    border-radius: 8px;
                    background-color: #ffffff;
                    box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
                }}
                .form-group {{
                    margin-bottom: 10px;
                }}
                .form-check-input {{
                    margin-right: 10px;
                }}
                .btn-primary {{
                    background-color: #007bff;
                    color: #ffffff;
                    border: none;
                    padding: 10px 20px;
                    border-radius: 4px;
                    cursor: pointer;
                }}
                .btn-primary:hover {{
                    background-color: #0056b3;
                }}
            </style>
        </head>
        <body>
            <div>
                <form class="selection_form" method="post">
                    <div class="form-group">
                        {'\n'.join(selection_buttons)}
                    </div>
                    <button type="submit" class="btn btn-primary">Save</button>
                </form>
            </div>
        </body>
        </html>
    '''
