create database AutoFacil;

create table Veiculos(
id integer(3), 
tipo varchar(20), 
categoria varchar(20), 
marca varchar(20), 
modelo varchar(20), 
transmissao varchar(20), 
precoDiario decimal(6, 2), 
nome varchar(20), 
imagem blob, 
nMalas integer(1), 
nPassageiros integer(1), 
nPortas integer(1),
combustivel varchar(20), 
status varchar(20)
);

select * from Veiculos
where marca = 'Hyundai';

drop table Veiculos;

insert into Veiculos(id, tipo, categoria, marca, modelo, transmissao, precoDiario, nome, imagem, nMalas, nPassageiros, nPortas, combustivel, status) values
(1, "econômico", "Econômico", "Fiat", "Mobi", "manual", 95.00, "Fiat Mobi", "https://production.autoforce.com/uploads/version/profile_image/10921/model_main_webp_comprar-like-1-0_9eee82ebb4.png.webp", 2, 5, 4, "Flex", "disponível"),
(2, "econômico", "Econômico","Renault", "Kwid", "manual", 100.00,"Renault Kwid","https://www.webmotors.com.br/imagens/prod/348031/RENAULT_KWID_1.0_12V_SCE_FLEX_OUTSIDER_MANUAL_34803110315083122.webp", 2, 5, 4, "Flex","disponível"),
(3, "econômico", "Econômico", "Hyundai", "HB20", "manual", 110.00, "Hyundai HB20", "/static/img/hb20.webp", 3, 5, 4, "Flex", "disponível"),
(4, "econômico", "Econômico", "Chevrolet", "Onix", "manual", 115.00, "Chevrolet Onix", "/static/img/onix.png", 3, 5, 4, "Flex", "disponível"),
(5, "econômico", "Econômico", "Volkswagen", "Gol", "manual", 105.00, "Volkswagen Gol", "https://cdn.motor1.com/images/mgl/YAAopq/s3/volkswagen-gol-1.0-2023.jpg", 2, 5, 4, "Flex", "disponível"),
(6, "sedan", "Sedan", "Toyota", "Corolla", "automático", 180.00, "Toyota Corolla", "/static/img/corolla.png", 3, 5, 4, "Gasolina", "disponível"),
(7, "sedan", "Sedan", "Honda", "Civic", "automático", 185.00, "Honda Civic", "https://di-uploads-pod33.dealerinspire.com/hendrickhondacharlotte/uploads/2021/03/mlp-img-top-2021-civic.png", 3, 5, 4, "Gasolina", "disponível"),
(8, "sedan", "Sedan", "Nissan", "Sentra", "automático", 170.00, "Nissan Sentra", "https://www.nissan-cdn.net/content/dam/Nissan/br/site/veiculos/sentra-my25/thumbs/sentra_exclusive_int_premium.png", 3, 5, 4, "Flex", "disponível"),
(9, "sedan", "Sedan", "Chevrolet", "Cruze", "automático", 175.00, "Chevrolet Cruze", "https://revistacarro.com.br/wp-content/uploads/2018/05/chevrolet_cruze_sport6_ltz.png", 3, 5, 4, "Flex", "disponível"),
(10, "sedan", "Sedan", "Volkswagen", "Virtus", "automático", 165.00, "Volkswagen Virtus", "https://cadastro.motorleads.co/public/images/20240130022136-v5.png", 3, 5, 4, "Flex", "disponível"),
(11, "suv", "SUV", "Jeep", "Compass", "automático", 220.00, "Jeep Compass", "https://www.webmotors.com.br/imagens/prod/348683/JEEP_COMPASS_1.3_T270_TURBO_FLEX_S_AT6_3486831606189095.webp?s=fill&w=170&h=125&t=true", 4, 5, 4, "Diesel", "disponível"),
(12, "suv", "SUV", "Hyundai", "Creta", "automático", 200.00, "Hyundai Creta", "https://www.webmotors.com.br/imagens/prod/348376/HYUNDAI_CRETA_1.6_16V_FLEX_ACTION_AUTOMATICO_34837618173811432.webp", 3, 5, 4, "Flex", "disponível"),
(13, "suv", "SUV", "Honda", "HR-V", "automático", 210.00, "Honda HR-V", "https://production.autoforce.com/uploads/version/profile_image/9408/comprar-exl-honda-sensing_f6ae5428c9.png", 3, 5, 4, "Gasolina", "disponível"),
(14, "suv", "SUV", "Nissan", "Kicks", "automático", 195.00, "Nissan Kicks", "https://www.nissan.com.br/content/dam/Nissan/br/site/veiculos/kicks-play/360/advance/branco-diamond/01.png.ximg.c1h.360.png", 3, 5, 4, "Flex", "disponível"),
(15, "suv", "SUV", "Chevrolet", "Tracker", "automático", 205.00, "Chevrolet Tracker", "https://www.autoclachevrolet.com.br/content/dam/chevrolet/sa/br/pt/master/home/suvs/tracker/tracker-myr-2026/2-colorizer/lt-at-turbo/chevrolet-tracker-lt-preto-ouro-negro.jpg?imwidth=1920", 3, 5, 4, "Flex", "disponível"),
(16, "luxo", "Luxo", "BMW", "Série 3", "automático", 450.00, "BMW Série 3", "https://www.bmw.com.br/content/dam/bmw/common/all-models/3-series/sedan/2024/navigation/bmw-	3-series-ice-lci-modelfinder.png", 4, 5, 4, "Gasolina", "disponível"),
(17, "luxo", "Luxo", "Audi", "A4", "automático", 460.00, "Audi A4", "https://www.webmotors.com.br/imagens/prod/379665/AUDI_A4_2.0_TFSI_MHEV_S_LINE_QUATTRO_S_TRONIC_37966510582707039.webp", 4, 5, 4, "Gasolina", "disponível"),
(18, "luxo", "Luxo", "Mercedes-Benz", "C180", "automático", 480.00, "Mercedes-Benz C180", "https://www.webmotors.com.br/imagens/prod/347940/MERCEDESBENZ_C_180_1.6_CGI_GASOLINA_SPORT_COUPE_9GTRONIC_34794009590838032.webp", 4, 5, 4, "Gasolina", "disponível"),
(19, "luxo", "Luxo", "Volvo", "XC60", "automático", 500.00, "Volvo XC60", "https://www.webmotors.com.br/imagens/prod/348860/VOLVO_XC60_2.0_T8_RECHARGE_POLESTAR_ENGINEERED_AWD_GEARTRONIC_34886011041803311.webp", 4, 5, 4, "Híbrido", "disponível"),
(20, "luxo", "Luxo", "Jaguar", "XE", "automático", 520.00, "Jaguar XE", "https://www.webmotors.com.br/imagens/prod/348195/JAGUAR_XE_2.0_16V_INGENIUM_P250_GASOLINA_RDYNAMIC_S_4P_AUTOMATICO_34819510562480227.webp", 4, 5, 4, "Gasolina", "disponível");

CREATE TABLE Cliente (
  Id_Cliente INT PRIMARY KEY AUTO_INCREMENT,
  Email VARCHAR(100) NOT NULL,
  CNH VARCHAR(20),
  CPF CHAR(11) UNIQUE NOT NULL,
  Nome VARCHAR(100) NOT NULL,
  Telefone VARCHAR(15),
  Data_Nascimento DATE
);

CREATE TABLE Endereco (
  Id_Endereco INT PRIMARY KEY AUTO_INCREMENT,
  Id_Cliente INT,
  Logradouro VARCHAR(100),
  Estado CHAR(2),
  Cidade VARCHAR(50),
  CEP CHAR(8),
  Tipo VARCHAR(20),
  FOREIGN KEY (Id_Cliente) REFERENCES Cliente(Id_Cliente)
);

CREATE TABLE Usuario (
  Id_Usuario INT PRIMARY KEY AUTO_INCREMENT,
  Id_Cliente INT,
  Login VARCHAR(50) UNIQUE NOT NULL,
  Senha VARCHAR(100) NOT NULL,
  Tipo VARCHAR(20),
  Ultimo_Acesso DATETIME,
  FOREIGN KEY (Id_Cliente) REFERENCES Cliente(Id_Cliente)
);

CREATE TABLE Funcionarios (
  Id_Funcionario INT PRIMARY KEY AUTO_INCREMENT,
  Nome VARCHAR(100) NOT NULL,
  Cargo VARCHAR(50),
  Salario DECIMAL(10,2),
  Email VARCHAR(100),
  Telefone VARCHAR(15)
);

CREATE TABLE Frota (
  Id_Veiculo INT PRIMARY KEY AUTO_INCREMENT,
  Status VARCHAR(20)
);

CREATE TABLE Manutencoes (
  Id_Manutencao INT PRIMARY KEY AUTO_INCREMENT,
  Id_Veiculo INT,
  Tipo VARCHAR(50),
  Data DATE,
  Descricao TEXT,
  Custo DECIMAL(10,2),
  FOREIGN KEY (Id_Veiculo) REFERENCES Frota(Id_Veiculo)
);

CREATE TABLE Multas (
  Id_Multa INT PRIMARY KEY AUTO_INCREMENT,
  Id_Veiculo INT,
  Data DATE,
  Valor DECIMAL(10,2),
  Descricao TEXT,
  Status VARCHAR(20),
  FOREIGN KEY (Id_Veiculo) REFERENCES Frota(Id_Veiculo)
);

CREATE TABLE Local_RetiradaDevolucao (
  Id_Local INT PRIMARY KEY AUTO_INCREMENT,
  Endereco VARCHAR(100),
  Horario VARCHAR(50),
  Nome VARCHAR(50)
);

CREATE TABLE Planos (
  Id_Planos INT PRIMARY KEY AUTO_INCREMENT,
  Nome VARCHAR(50),
  Descricao TEXT,
  Preco DECIMAL(10,2)
);

CREATE TABLE Pagamentos (
  Id_Pagamento INT PRIMARY KEY AUTO_INCREMENT,
  Id_Aluguel INT,
  Forma_Pagamento VARCHAR(30),
  Data DATE,
  Valor DECIMAL(10,2),
  Status VARCHAR(20),
  Campo_6 VARCHAR(50),
  Campo VARCHAR(50),
  FOREIGN KEY (Id_Aluguel) REFERENCES Frota(Id_Veiculo)
);

CREATE TABLE Avaliacoes (
  Id_Avaliacao INT PRIMARY KEY AUTO_INCREMENT,
  Id_Usuario INT,
  Id_Cliente INT,
  Nota INT CHECK (Nota BETWEEN 0 AND 10),
  Comentario TEXT,
  Data DATE,
  FOREIGN KEY (Id_Usuario) REFERENCES Usuario(Id_Usuario),
  FOREIGN KEY (Id_Cliente) REFERENCES Cliente(Id_Cliente)
);
