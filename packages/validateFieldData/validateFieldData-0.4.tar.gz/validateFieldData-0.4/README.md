# ValidateFieldData

validateFieldData is a Python library for file cleaner. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install validateData.

```bash
pip install validateFieldData
```

## Usage

```python
import validateFieldData as mp


# text = '   Hola   '
mp.validateField(text)
# returns 'Hola'

# username =  ' Dark Sider12 '
mp.validateField(username, capitalize = 'lowercase', spaces =True)
# returns 'darksider12'

# username =  ' Dark Sider12 '
mp.validateField(username, capitalize = 'lowercase')
# returns 'dark sider12'

# username =  ' Dark Sider12 '
mp.validateField(username, spaces =True)
# returns 'DarkSider12'

# first_name =  ' Dark Sider12 '
mp.validateField(first_name,capitalize = 'uppercase')
# returns 'DARK SIDER12'

# work_email = 'nologin@gmail'
mp.validateField(work_email, email = True)
# returns 'EL correo no es valido '

# comments = '   Este texto tiene menos de 300 caracteres    '
mp.validateField(comments,length =300)
# returns 'Este texto tiene menos de 300 caracteres'

# My_Document = '1064 578923'
mp.validateField(My_Document, document = True)
# returns '1064578923'

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)