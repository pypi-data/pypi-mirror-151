# PowerI2c

PowerI2c es una libreria que establece una conexion I2C entre una raspberry pi 4 y un arduino, donde se pueden enviar comandos al arduino y recibir datos de tipo float. 

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install PowerI2C
```

## Usage
La libreria consta de 4 comandos, init accede a un menu desde el cual se pueden obtener los valores de voltaje, corriente o potencia y los 3 comandos faltantes imprimen por consola los valores de voltaje, corriente o potencia.
```python
from PowerI2C import PowerI2C

PowerI2C.init()   #Ejecuta el codigo tipo menu
PowerI2C.getVoltage() 
PowerI2C.getCurrent()  
PowerI2C.getPower()
```

## Contributing
Las contribuciones son bienvenidas.

## License
[MIT](https://choosealicense.com/licenses/mit/)

