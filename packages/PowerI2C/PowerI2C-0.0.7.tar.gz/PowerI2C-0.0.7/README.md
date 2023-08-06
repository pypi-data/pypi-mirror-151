# PowerI2c

PowerI2c es una libreria que establece una conexion I2C entre una raspberry pi 4 y un arduino, donde se pueden consultar 
valores de voltaje, corriente y potencia desde las Raspberry y recibir respuestas del Arduino. Se pueden obtener tanto 
los valores por el terminal como almacenar los valores en una variable.

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install foobar.

```bash
pip install PowerI2C
```

## Usage
La libreria consta de 7 comandos, init accede a un menu desde el cual se pueden obtener los valores de voltaje, corriente o potencia y los comandos con prefijo "get" retornan el valor en float de la variable solicitada, por ultimo 
los comandos print enseñan por consola los valores solicitados.
```python
from PowerI2C import PowerI2C

PowerI2C.init()   #Ejecuta el codigo tipo menu
PowerI2C.getVoltage() 
PowerI2C.getCurrent()  
PowerI2C.getPower()
PowerI2C.printVoltage()
PowerI2C.printCurrent()
PowerI2C.printPower()
```

## Contributing
Las contribuciones son bienvenidas.

## License
[MIT](https://choosealicense.com/licenses/mit/)

