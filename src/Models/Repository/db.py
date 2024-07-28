import sqlite3
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../Entities')))
from animal import (
    InfoAnimal,
    InfoResgate,
    Castracao,
    Obito,
    Exames,
    Vacinas,
    Vermifugos,
    Pesos,
    ProfilaxiaLaishmaniose,
    LarTemporario
)
from adotante import (
    Adotante,
    ObservacaoAdotante,
    AdocaoAdotante
)


class DataBaseAPAM:
	def __init__(self):
		self.create_tables()
		self.results_animal = self.db_execute("SELECT * FROM animal")
		self.results_animal_adotante = self.db_execute("SELECT * FROM animal_adotante")
		self.results_adotante = self.db_execute("SELECT * FROM adotante")
		self.results_acompanhamento_adocao = self.db_execute("SELECT * FROM acompanhamento_adocao")
		self.results_resgate = self.db_execute("SELECT * FROM resgate")
		self.results_castracao = self.db_execute("SELECT * FROM castracao")
		self.results_obito = self.db_execute("SELECT * FROM obito")
		self.results_exames = self.db_execute("SELECT * FROM exames")
		self.results_vacinas = self.db_execute("SELECT * FROM vacinas")
		self.results_vermifugos = self.db_execute("SELECT * FROM vermifugos")
		self.results_pesos = self.db_execute("SELECT * FROM pesos")
		self.results_profilaxia_laishmaniose = self.db_execute("SELECT * FROM profilaxia_laishmaniose")
		self.results_lar_temporario = self.db_execute("SELECT * FROM lar_temporario")
		


	def db_execute(self, query, param = []):
		with sqlite3.connect('GA_APAM.db') as con:
			cur = con.cursor()
			cur.execute(query, param)
			con.commit()
			return cur.fetchall()

	# para habilitar a chave estrangeira para o delete on cascade
	def enable_FOREIGN_keys(self):
		with sqlite3.connect('GA_APAM.db') as con:
			cur = con.cursor()
			cur.execute('PRAGMA foreign_keys = ON')
			con.commit()


	def create_tables(self):
		self.db_execute('''CREATE TABLE IF NOT EXISTS animal
		    (id_animal INTEGER PRIMARY KEY AUTOINCREMENT,
		    foto BLOB,
           	nome_animal TEXT NOT NULL,
		    data_cadastro DATE NOT NULL,
		    especie TEXT NOT NULL,
		    genero TEXT NOT NULL,
			temperamento TEXT NOT NULL,
		    idade_anos TEXT NOT NULL,
		    idade_meses TEXT NOT NULL,	
		    porte TEXT NOT NULL,
		    pelagem TEXT NOT NULL,
		    raca TEXT NOT NULL,
			microchip TEXT NOT NULL,
			status_atual TEXT NOT NULL,
			possui_sequela BOOLEAN,
			observacoes TEXT)''')
	

   
		self.db_execute('''CREATE TABLE IF NOT EXISTS animal_adotante
		    (id_animal_adotante INTEGER PRIMARY KEY AUTOINCREMENT,
		    id_animal INTEGER,
			id_adotante INTEGER,
		    data_adocao DATE NOT NULL,
			FOREIGN KEY (id_animal) REFERENCES animal(id_animal),
      		FOREIGN KEY (id_adotante) REFERENCES adotante(id_adotante))''')
   
		self.db_execute('''CREATE TABLE IF NOT EXISTS adotante
			(id_adotante INTEGER PRIMARY KEY AUTOINCREMENT,
			nome_adotante TEXT NOT NULL,
			rg TEXT NOT NULL,
			cpf TEXT,
			rua TEXT NOT NULL,
			numero TEXT NOT NULL,
   			bairro TEXT NOT NULL,
			cep TEXT NOT NULL,
			cidade TEXT NOT NULL,
			estado TEXT NOT NULL,
			email TEXT NOT NULL,
			profissao TEXT NOT NULL,
			telefone_fixo TEXT NOT NULL,
			telefone_celular TEXT NOT NULL,
			referencia_rua TEXT NOT NULL,
   			complemento TEXT NOT NULL)''')
   
		self.db_execute('''CREATE TABLE IF NOT EXISTS acompanhamento_adocao
			(id_acompanhamento_adocao INTEGER PRIMARY KEY AUTOINCREMENT,
      		id_adotante INTEGER,
      		observacoes TEXT NOT NULL,
           	data_observacao DATE NOT NULL,
            FOREIGN KEY (id_adotante) REFERENCES adotante(id_adotante))''')
   
		self.db_execute('''CREATE TABLE IF NOT EXISTS resgate
		    (id_resgate INTEGER PRIMARY KEY AUTOINCREMENT,
		    id_animal INTEGER,
		    local_resgate TEXT NOT NULL,
		    atendimento TEXT NOT NULL,
		    necessario_intervencao_cirurgica TEXT NOT NULL,
		    destinacao_do_protegido TEXT NOT NULL,
		    historico_anamnese TEXT NOT NULL,
		    diagnostico_estado_saude TEXT NOT NULL,
		    tratamento_intervencao_e_medicacao TEXT NOT NULL,
		    data_resgate DATE NOT NULL,
			observacoes TEXT NOT NULL,
		    FOREIGN KEY (id_animal) REFERENCES animal(id_animal) ON DELETE CASCADE)''')

		self.db_execute('''CREATE TABLE IF NOT EXISTS castracao
			(id_animal INTEGER NOT NULL,
			castrado BOOLEAN NOT NULL,
			data_castracao DATE NOT NULL,
      		FOREIGN KEY (id_animal) REFERENCES animal(id_animal) ON DELETE CASCADE)''')
   
		self.db_execute('''CREATE TABLE IF NOT EXISTS obito
			(id_animal INTEGER NOT NULL,
			data_obito DATE NOT NULL,
	  		FOREIGN KEY (id_animal) REFERENCES animal(id_animal) ON DELETE CASCADE)''')
   
		self.db_execute('''CREATE TABLE IF NOT EXISTS exames
			(id_exame INTEGER PRIMARY KEY AUTOINCREMENT,
			id_animal INTEGER,
			data_exame DATE NOT NULL,
			exames_realizados TEXT NOT NULL,
			medicacoes TEXT NOT NULL,
			tratamento TEXT NOT NULL,
			alimentacao_especial TEXT NOT NULL,
			observacoes TEXT NOT NULL,
			FOREIGN KEY (id_animal) REFERENCES animal(id_animal) ON DELETE CASCADE)''')
						
		self.db_execute('''CREATE TABLE IF NOT EXISTS vacinas
			(id_vacinas INTEGER PRIMARY KEY AUTOINCREMENT,
			id_animal INTEGER,
			vacina TEXT NOT NULL,
            data_vacina DATE NOT NULL,
			data_proxima_dose DATE NOT NULL,
			FOREIGN KEY (id_animal) REFERENCES animal(id_animal) ON DELETE CASCADE)''')
			
		self.db_execute('''CREATE TABLE IF NOT EXISTS vermifugos
			(id_vermifugos INTEGER PRIMARY KEY AUTOINCREMENT,
      		id_animal INTEGER,
           	data_aplicacao DATE NOT NULL,
            data_proxima_aplicacao DATE NOT NULL,
            FOREIGN KEY (id_animal) REFERENCES animal(id_animal))''')

		self.db_execute('''CREATE TABLE IF NOT EXISTS pesos
			(id_pesos INTEGER PRIMARY KEY AUTOINCREMENT,
			id_animal INTEGER,
			peso FLOAT NOT NULL,
			data_peso DATE NOT NULL,
			data_proximo_peso DATE NOT NULL,
			FOREIGN KEY (id_animal) REFERENCES animal(id_animal) ON DELETE CASCADE)''')
   
		self.db_execute('''CREATE TABLE IF NOT EXISTS profilaxia_laishmaniose
			(id_profilaxia INTEGER PRIMARY KEY AUTOINCREMENT,
			id_animal INTEGER,
			data_aplicacao DATE NOT NULL,
			data_proxima_aplicacao DATE NOT NULL,
			FOREIGN KEY (id_animal) REFERENCES animal(id_animal) ON DELETE CASCADE)''')

		self.db_execute('''CREATE TABLE IF NOT EXISTS lar_temporario
			(id_lar_temporario INTEGER PRIMARY KEY AUTOINCREMENT,
			id_animal INTEGER,
			local TEXT NOT NULL,
			data_entrada DATE NOT NULL,
			data_saida DATE NOT NULL,
			FOREIGN KEY (id_animal) REFERENCES animal(id_animal) ON DELETE CASCADE)''')
   
	
	# CRUD referente ao animal
	# Resgate
	def add_resgate(self, resgate: InfoResgate) -> None:
		sql = '''INSERT INTO resgate (id_animal, local_resgate, atendimento, necessario_intervencao_cirurgica, destinacao_do_protegido, historico_anamnese, diagnostico_estado_saude, tratamento_intervencao_e_medicacao, data_resgate, observacoes) 
  				 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
		self.db_execute(sql, (resgate.id_animal, resgate.local_resgate, resgate.atendimento, resgate.necessario_intervencao_cirurgica, resgate.destinacao_do_protegido, resgate.historico_anamnese, resgate.diagnostico_estado_saude, resgate.tratamento_intervencao_e_medicacao, resgate.data_resgate, resgate.observacoes))
  
	def get_resgate(self, id_animal: int) -> list:
		sql = '''SELECT * FROM resgate WHERE id_animal = ?'''
		return self.db_execute(sql, [id_animal])

	def update_resgate(self, resgate: InfoResgate) -> None:
		sql = '''UPDATE resgate
				SET local_resgate = ?, atendimento = ?, necessario_intervencao_cirurgica = ?, destinacao_do_protegido = ?, historico_anamnese = ?, diagnostico_estado_saude = ?, tratamento_intervencao_e_medicacao = ?, data_resgate = ?, observacoes = ?
				WHERE id_animal = ?'''
		self.db_execute(sql, (resgate.local_resgate, resgate.atendimento, resgate.necessario_intervencao_cirurgica, resgate.destinacao_do_protegido, resgate.historico_anamnese, resgate.diagnostico_estado_saude, resgate.tratamento_intervencao_e_medicacao, resgate.data_resgate, resgate.observacoes, resgate.id_animal))
  
	def delete_resgate(self, id_animal: int) -> None:
		sql = '''DELETE FROM resgate WHERE id_animal = ?'''
		self.db_execute(sql, [id_animal])
  
	# Animal
	def add_animal(self, animal: InfoAnimal) -> None:
		sql = '''INSERT INTO animal (foto, nome_animal, data_cadastro, especie, genero, temperamento, idade_anos, idade_meses, porte, pelagem, raca, microchip, status_atual, possui_sequela, observacoes) 
  				 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
		self.db_execute(sql, (animal.foto, animal.nome_animal, animal.data_cadastro, animal.especie, animal.genero, animal.temperamento, animal.idade_anos, animal.idade_meses, animal.porte, animal.pelagem, animal.raca, animal.microchip, animal.status_atual, animal.possui_sequela, animal.observacoes))

	def get_all_animals(self) -> list:
		sql = '''SELECT * FROM animal'''
		return self.db_execute(sql)

	def get_animais(self, nome: str) -> list:
		sql = '''SELECT * FROM animal WHERE nome_animal = ?'''
		return self.db_execute(sql, [nome])

	def update_animal(self, id_animal: int, animal: InfoAnimal) -> None:
		sql = '''UPDATE animal
                SET foto = ?, nome_animal = ?, data_cadastro = ?, especie = ?, genero = ?, temperamento = ?, idade_anos = ?, idade_meses = ?, porte = ?, pelagem = ?, raca = ?, microchip = ?, status_atual = ?, possui_sequela = ?, observacoes = ?
                WHERE id_animal = ?'''
		self.db_execute(sql, (animal.foto, animal.nome_animal, animal.data_cadastro, animal.especie, animal.genero, animal.temperamento, animal.idade_anos, animal.idade_meses, animal.porte, ','.join(animal.pelagem), animal.raca, animal.microchip, animal.status_atual, animal.possui_sequela, animal.observacoes, id_animal))
        
	def delete_animal(self, id_animal: int) -> None:
		sql = '''DELETE FROM animal WHERE id_animal = ?'''
		self.db_execute(sql, [id_animal])
	
	# CRUD referente aos atributos do animal
	# Castraçao
	def add_castracao(self, castracao: Castracao) -> None:
		sql = '''INSERT INTO castracao (id_animal, data_castracao, castrado) VALUES (?, ?, ?)'''
		self.db_execute(sql, (castracao.id_animal, castracao.data_castracao, castracao.castrado))
  
	def get_castracao(self, id_animal: int) -> list:
		sql = '''SELECT * FROM castracao WHERE id_animal = ?'''
		return self.db_execute(sql, [id_animal])

	def update_castracao(self, castracao: Castracao) -> None:
		sql = '''UPDATE castracao SET data_castracao = ?, castrado = ? WHERE id_animal = ?'''
		self.db_execute(sql, (castracao.data_castracao, castracao.castrado, castracao.id_animal))
  
	def delete_castracao(self, id_animal: int) -> None:
		sql = '''DELETE FROM castracao WHERE id_animal = ?'''
		self.db_execute(sql, [id_animal])
  
	# Obito
	def add_obito(self, obito: Obito) -> None:
		sql = '''INSERT INTO obito (id_animal, data_obito) VALUES (?, ?)'''
		self.db_execute(sql, (obito.id_animal, obito.data_obito))
  
	def get_obito(self, id_animal: int) -> list:
		sql = '''SELECT * FROM obito WHERE id_animal = ?'''
		return self.db_execute(sql, [id_animal])

	def update_obito(self, obito: Obito) -> None:
		sql = '''UPDATE obito SET data_obito = ? WHERE id_animal = ?'''
		self.db_execute(sql, (obito.data_obito, obito.id_animal))
	
	def delete_obito(self, id_animal: int) -> None:
		sql = '''DELETE FROM obito WHERE id_animal = ?'''
		self.db_execute(sql, [id_animal])
	
	# Exames
	def add_exames(self, exames: Exames) -> None:
		sql = '''INSERT INTO exames (id_animal, data_exame, exames_realizados, medicacoes, tratamento, alimentacao_especial, observacoes) VALUES (?, ?, ?, ?, ?, ?, ?)'''
		self.db_execute(sql, (exames.id_animal, exames.data_exame, exames.exames_realizados, exames.medicacoes, exames.tratamento, exames.alimentacao_especial, exames.observacoes))
	
	def get_exames(self, id_animal: int) -> list:
		sql = '''SELECT * FROM exames WHERE id_animal = ?'''
		return self.db_execute(sql, [id_animal])

	def update_exames(self, exames: Exames) -> None:
		sql = '''UPDATE exames SET data_exame = ?, exames_realizados = ?, medicacoes = ?, tratamento = ?, alimentacao_especial = ?, observacoes = ? WHERE id_animal = ?'''
		self.db_execute(sql, (exames.data_exame, exames.exames_realizados, exames.medicacoes, exames.tratamento, exames.alimentacao_especial, exames.observacoes, exames.id_animal))
  
	def delete_exames(self, id_animal: int) -> None:
		sql = '''DELETE FROM exames WHERE id_animal = ?'''
		self.db_execute(sql, [id_animal])
  
	# Vacinas
	def add_vacinas(self, vacinas: Vacinas) -> None:
		sql = '''INSERT INTO vacinas (id_animal, vacina, data_vacina, data_proxima_dose) VALUES (?, ?, ?, ?)'''
		self.db_execute(sql, (vacinas.id_animal, vacinas.vacina, vacinas.data_vacina, vacinas.data_proxima_dose))
  
	def get_vacinas(self, id_animal: int) -> list:
		sql = '''SELECT * FROM vacinas WHERE id_animal = ?'''
		return self.db_execute(sql, [id_animal])

	def update_vacinas(self, vacinas: Vacinas) -> None:
		sql = '''UPDATE vacinas SET vacina = ?, data_vacina = ?, data_proxima_dose = ? WHERE id_animal = ?'''
		self.db_execute(sql, (vacinas.vacina, vacinas.data_vacina, vacinas.data_proxima_dose, vacinas.id_animal))

	def delete_vacinas(self, id_animal: int) -> None:
		sql = '''DELETE FROM vacinas WHERE id_animal = ?'''
		self.db_execute(sql, [id_animal])
  
	# Vermifugos
	def add_vermifugos(self, vermifugos: Vermifugos) -> None:
		sql = '''INSERT INTO vermifugos (id_animal, data_aplicacao, data_proxima_aplicacao) VALUES (?, ?, ?)'''
		self.db_execute(sql, (vermifugos.id_animal, vermifugos.data_aplicacao, vermifugos.data_proxima_aplicacao))
	
	def get_vermifugos(self, id_animal: int) -> list:
		sql = '''SELECT * FROM vermifugos WHERE id_animal = ?'''
		return self.db_execute(sql, [id_animal])

	def update_vermifugos(self, vermifugos: Vermifugos) -> None:
		sql = '''UPDATE vermifugos SET data_aplicacao = ?, data_proxima_aplicacao = ? WHERE id_animal = ?'''
		self.db_execute(sql, (vermifugos.data_aplicacao, vermifugos.data_proxima_aplicacao, vermifugos.id_animal))
  
	def delete_vermifugos(self, id_animal: int) -> None:
		sql = '''DELETE FROM vermifugos WHERE id_animal = ?'''
		self.db_execute(sql, [id_animal])
  
	# Pesos
	def add_pesos(self, pesos: Pesos) -> None:
		sql = '''INSERT INTO pesos (id_animal, peso, data_peso, data_proximo_peso) VALUES (?, ?, ?, ?)'''
		self.db_execute(sql, (pesos.id_animal, pesos.peso, pesos.data_peso, pesos.data_proximo_peso))
	
	def get_pesos(self, id_animal: int) -> list:
		sql = '''SELECT * FROM pesos WHERE id_animal = ?'''
		return self.db_execute(sql, [id_animal])

	def update_pesos(self, pesos: Pesos) -> None:
		sql = '''UPDATE pesos SET peso = ?, data_peso = ?, data_proximo_peso = ? WHERE id_animal = ?'''
		self.db_execute(sql, (pesos.peso, pesos.data_peso, pesos.data_proximo_peso, pesos.id_animal))
  
	def delete_pesos(self, id_animal: int) -> None:
		sql = '''DELETE FROM pesos WHERE id_animal = ?'''
		self.db_execute(sql, [id_animal])
  
	# Profilaxia Laishmaniose
	def add_profilaxia_laishmaniose(self, profilaxia: ProfilaxiaLaishmaniose) -> None:
		sql = '''INSERT INTO profilaxia_laishmaniose (id_animal, data_aplicacao, data_proxima_aplicacao) VALUES (?, ?, ?)'''
		self.db_execute(sql, (profilaxia.id_animal, profilaxia.data_aplicacao, profilaxia.data_proxima_aplicacao))
  
	def get_profilaxia_laishmaniose(self, id_animal: int) -> list:
		sql = '''SELECT * FROM profilaxia_laishmaniose WHERE id_animal = ?'''
		return self.db_execute(sql, [id_animal])

	def update_profilaxia_laishmaniose(self, profilaxia: ProfilaxiaLaishmaniose) -> None:
		sql = '''UPDATE profilaxia_laishmaniose SET data_aplicacao = ?, data_proxima_aplicacao = ? WHERE id_animal = ?'''
		self.db_execute(sql, (profilaxia.data_aplicacao, profilaxia.data_proxima_aplicacao, profilaxia.id_animal))
  
	def delete_profilaxia_laishmaniose(self, id_animal: int) -> None:
		sql = '''DELETE FROM profilaxia_laishmaniose WHERE id_animal = ?'''
		self.db_execute(sql, [id_animal])
  
	# Lar Temporario
	def add_lar_temporario(self, lar: LarTemporario) -> None:
		sql = '''INSERT INTO lar_temporario (id_animal, local, data_entrada, data_saida) VALUES (?, ?, ?, ?)'''
		self.db_execute(sql, (lar.id_animal, lar.local, lar.data_entrada, lar.data_saida))
  
	def get_lar_temporario(self, id_animal: int) -> list:
		sql = '''SELECT * FROM lar_temporario WHERE id_animal = ?'''
		return self.db_execute(sql, [id_animal])

	def update_lar_temporario(self, lar: LarTemporario) -> None:
		sql = '''UPDATE lar_temporario SET local = ?, data_entrada = ?, data_saida = ? WHERE id_animal = ?'''
		self.db_execute(sql, (lar.local, lar.data_entrada, lar.data_saida, lar.id_animal))
  
	def delete_lar_temporario(self, id_animal: int) -> None:
		sql = '''DELETE FROM lar_temporario WHERE id_animal = ?'''
		self.db_execute(sql, [id_animal])

	# CRUD referente aos atributos do adotante
	# Adotante
	def add_adotante(self, adotante: Adotante) -> None:
		sql = '''INSERT INTO adotante (nome_adotante, rg, cpf, rua, numero, bairro, cep, cidade, estado, email, profissao, telefone_fixo, telefone_celular, referencia_rua, complemento) 
  				 VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
		self.db_execute(sql, (adotante.nome_adotante, adotante.rg, adotante.cpf, adotante.rua, adotante.numero, adotante.bairro, adotante.cep, adotante.cidade, adotante.estado, adotante.email, adotante.profissao, adotante.telefone_fixo, adotante.telefone_celular, adotante.referencia_rua, adotante.complemento))
  
	def get_adotante(self, id_adotante: int) -> list:
		sql = '''SELECT * FROM adotante WHERE id_adotante = ?'''
		return self.db_execute(sql, [id_adotante])

	def update_adotante(self, id_adotante: int, adotante: Adotante) -> None:
		sql = '''UPDATE adotante
				SET nome_adotante = ?, rg = ?, cpf = ?, rua = ?, numero = ?, bairro = ?, cep = ?, cidade = ?, estado = ?, email = ?, profissao = ?, telefone_fixo = ?, telefone_celular = ?, referencia_rua = ?, complemento = ?
				WHERE id_adotante = ?'''
		self.db_execute(sql, (adotante.nome_adotante, adotante.rg, adotante.cpf, adotante.rua, adotante.numero, adotante.bairro, adotante.cep, adotante.cidade, adotante.estado, adotante.email, adotante.profissao, adotante.telefone_fixo, adotante.telefone_celular, adotante.referencia_rua, adotante.complemento, id_adotante))
	
	def delete_adotante(self, id_adotante: int) -> None:
		sql = '''DELETE FROM adotante WHERE id_adotante = ?'''
		self.db_execute(sql, [id_adotante])
  
	# Observacao Adotante
	def add_acompanhamento_adocao(self, observacao: ObservacaoAdotante) -> None:
		sql = '''INSERT INTO acompanhamento_adocao (id_adotante, observacao, data_observacao) VALUES (?, ?, ?)'''
		self.db_execute(sql, (observacao.id_adotante, observacao.observacao, observacao.data_observacao))
	
	def get_acompanhamento_adocao(self, id_adotante: int) -> list:
		sql = '''SELECT * FROM acompanhamento_adocao WHERE id_adotante = ?'''
		return self.db_execute(sql, [id_adotante])

	def update_acompanhamento_adocao(self, observacao: ObservacaoAdotante) -> None:
		sql = '''UPDATE acompanhamento_adocao SET observacao = ?, data_observacao = ? WHERE id_adotante = ?'''
		self.db_execute(sql, (observacao.observacao, observacao.data_observacao, observacao.id_adotante))
  
	def delete_acompanhamento_adocao(self, id_adotante: int) -> None:
		sql = '''DELETE FROM acompanhamento_adocao WHERE id_adotante = ?'''
		self.db_execute(sql, [id_adotante])
  
	# Adocao Adotante
 
	def add_adocao_adotante(self, adocao: AdocaoAdotante) -> None:
		sql = '''INSERT INTO animal_adotante (id_animal, id_adotante, data_adocao) VALUES (?, ?, ?)'''
		self.db_execute(sql, (adocao.id_animal, adocao.id_adotante, adocao.data_adocao))
	
	def get_adocao_adotante(self, id_animal: int) -> list:
		sql = '''SELECT * FROM animal_adotante WHERE id_animal = ?'''
		return self.db_execute(sql, [id_animal])

	def update_adocao_adotante(self, adocao: AdocaoAdotante) -> None:
		sql = '''UPDATE animal_adotante SET id_adotante = ?, data_adocao = ? WHERE id_animal = ?'''
		self.db_execute(sql, (adocao.id_adotante, adocao.data_adocao, adocao.id_animal))
  
	def delete_adocao_adotante(self, id_animal: int) -> None:
		sql = '''DELETE FROM animal_adotante WHERE id_animal = ?'''
		self.db_execute(sql, [id_animal])
  
if __name__ == "__main__":
    db = DataBaseAPAM()
    print("Banco de dados e tabelas criados com sucesso.")