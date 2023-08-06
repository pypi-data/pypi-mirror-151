# ValidateFieldData

validateFieldData is a Python library For cleaning up data related to, or to be submitted in  form fields. 

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
mp.validateField(username, capitalization = 'lowercase', spaces =True)
# returns 'darksider12'

# username =  ' Dark Sider12 '
mp.validateField(username, capitalization = 'lowercase')
# returns 'dark sider12'

# username =  ' Dark Sider12 '
mp.validateField(username, spaces =True)
# returns 'DarkSider12'

# first_name =  ' Dark Sider12 '
mp.validateField(first_name,capitalization = 'uppercase')
# returns 'DARK SIDER12'

# work_email = 'nologin@gmail'
mp.validateField(work_email, email = True)
# returns 'EL correo no es valido '

# comments = '   Este texto tiene menos de 300 caracteres    '
mp.validateField(comments,length =300)
# returns 'Este texto tiene menos de 300 caracteres'

# ID_number = ' 1064 78923 '
mp.validateField(ID_number, document = True)
# returns '1064578923'

```

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[MIT](https://choosealicense.com/licenses/mit/)