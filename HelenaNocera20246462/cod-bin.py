import sys
import re

OPCODES = {
    "add":  "0000", "sub":  "0001", "mul":  "0010", "div":  "0011",
    "sll":  "0100", "slr":  "0101", "and":  "0110", "or":   "0111",
    "xor":  "1000", "addi": "1001", "lw":   "1010", "sw":   "1011",
    "jal":  "1100", "jalr": "1101", "brzr": "1110", "not":  "1111"
}

def registrar_para_binario(reg_str, bits=4):

    if not re.match(r'^x([0-9]|1[0-5])$', reg_str):
        raise ValueError(f"Registrador inválido: '{reg_str}'. Esperado x0-x15.")
    
    num = int(reg_str[1:]) 
    return format(num, f'0{bits}b') 


def imediato_para_binario(num_str, bits=4): 

    num = int(num_str)
    if not (-(2**(bits-1)) <= num < (2**(bits-1))):
            raise ValueError(f"Valor imediato '{num_str}' fora do intervalo para {bits} bits ({- (2**(bits-1))} a {(2**(bits-1))-1}).")

    if num < 0:
        num = (1 << bits) + num 
    
    return format(num, f'0{bits}b')


def processar_instrucao(linha):

    linha = linha.strip()
    if not linha or linha.startswith(';'):
        return None

    partes = linha.split()
    if not partes:
        return None

    instrucao_nome = partes[0].lower()

    if instrucao_nome not in OPCODES:
        raise ValueError(f"Instrução não reconhecida: '{instrucao_nome}'. Linha: '{linha}'")

    opcode_bin = OPCODES[instrucao_nome]
    

    if len(partes) != 3:
        raise ValueError(f"Formato inválido para '{instrucao_nome}'. Esperado '{instrucao_nome} Op1 Op2'.")
    
    op1_rd = registrar_para_binario(partes[1])
    
    if instrucao_nome in ["add", "sub", "div", "sll", "slr", "and", "or", "xor", "jalr", "brzr", "lw", "sw", "mul", "not"]:
        op2_rs = registrar_para_binario(partes[2])
        return f"{opcode_bin}{op1_rd}{op2_rs}" 

    elif instrucao_nome in ["addi", "jal"]:
        op2_imm = imediato_para_binario(partes[2], bits=4) 
        return f"{opcode_bin}{op1_rd}{op2_imm}"
    

def main():
    arquivo_entrada_path = sys.argv[1]

    with open(arquivo_entrada_path, 'r') as f_in:
        for i, linha in enumerate(f_in):
            opcode_binario = processar_instrucao(linha)
            if opcode_binario:
                print(opcode_binario)


if __name__ == "__main__":
    main()
