# Trabalho 2 de Fundamento de Sistemas Embarcados


**Nome** | **Matricula** | **GitHub** 
---------|:-------------:|:----------:
| Lucas Ganda | 170039668 | lucasgandac

## Sobre

Este trabalho tem por objetivo a implementação de um sistema (que simula) o controle de um forno para soldagem de placas de circuito impresso (PCBs).

## Execução

A execução é bastante simples, para executar a aplicação basta apenas estar na pasta do projeto e rodar os comando

```
python3 main.py
```

Obs : Apesar do bug na gravaçao, a definição das variaveis Ki, Kp e Kd manualmente está funcionando corretamente

## Vídeo
Segue link do vídeo com gravação da apresentação do trabalho <br>
[Link da apresentação](https://youtu.be/qEHHe5WtQpw)

## Imagens

Segue print das curvas de aquecimento

O de cima mostra a curva de sinal de controle no maximo, pois a temperatura interna está longe da de referência, enquanto no de baixo é possível ver a queda do sinal, chegando inclusive a valores negativos, pois a temperatura interna está se igualando à de referência.


<img src="https://github.com/lucasgandac/Trabalho-2-FSE/blob/main/images/forno-init.png" alt="drawing" width="360"/>
<img src="https://github.com/lucasgandac/Trabalho-2-FSE/blob/main/images/forno.png" alt="drawing" width="360"/>
