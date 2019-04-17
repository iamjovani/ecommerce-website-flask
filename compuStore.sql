/*======================= CompuStore Main Database ===================================================*/

create database CompuStore;
use CompuStore;

/* CustomerAccount(account_id, email, password,  fname, lname, gender, date_of_birth, street, city, parish, telephone, created_on) */
create table CustomerAccount(
	account_id int auto_increment not null,
	email varchar(100),
	password varchar(255) not null,
	fname varchar(30) not null,
	lname varchar(30) not null,
	gender enum('Female','Male') not null,
	date_of_birth Date not null,
	street varchar(100) not null,
	city varchar(100) not null,
	parish varchar(100) not null,
	telephone varchar(20),
	created_on Date not null,
	primary key(account_id) 
);

/* CreditCardDetails(card_num, name_on_card, card_security_code, expiration_month, expiration_year, billing_street, billing_city, billing_parish) */
create table CreditCardDetails(
	card_num bigint(16) not null,
	name_on_card varchar(100),
	card_security_code int,
	expiration_month varchar(10) not null,
	expiration_year varchar(10) not null,
	billing_street varchar(100) not null,
	billing_city varchar(100) not null,
	billing_parish varchar(100) not null,
	primary key(card_num) 
);

/*CustomerCreditCard(account_id, card_num)*/
create table CustomerCreditCard(
	account_id int not null,
	card_num bigint(11) not null,
	primary key(account_id, card_num),
	foreign key(account_id) references CustomerAccount(account_id) on DELETE cascade on UPDATE cascade,
	foreign key(card_num) references CreditCardDetails(card_num) on DELETE cascade on UPDATE cascade
);

/* Branch(branch_id, name, street, city, parish, telephone) */
create table Branch(
	branch_id varchar(50) not null,
	name varchar(100) not null, 
	street varchar(100) not null,
	city varchar(100) not null,
	parish varchar(100) not null,
	telephone varchar(20) not null,
	primary key(branch_id)
);

/* LaptopModel(model_id, model, brand, cpu_specs, display_size, resolution, operating_system, gpu_specs, launch_date, thumbnail, price) */
create table LaptopModel(
	model_id varchar(100) not null,
	model text not null,
	brand varchar(100) not null,
	cpu_specs text, 
	display_size double(5,2), 
	resolution varchar(100),
	operating_system text,
	gpu_specs text,
	launch_date date,
	thumbnail text,
	price double(10,2) not null,
	primary key(model_id) 
);

/* ShoppingCart(cart_id, item_count, value)*/
create table ShoppingCart(
	cart_id int not null,
	item_count int not null,
	value double(20,2) not null,
	primary key(cart_id)
);

/* CustomerCart(account_id, cart_id) */
create table CustomerCart(
	account_id int not null,
	cart_id int not null,
	primary key(account_id, cart_id),
	foreign key(account_id) references CustomerAccount(account_id) on DELETE cascade on UPDATE cascade,
	foreign key(cart_id) references ShoppingCart(cart_id) on DELETE cascade on UPDATE cascade
);


/* CartItems(cart_id, model_id, quantity, cost, date_added) */
create table CartItems(
	cart_id int not null,
	model_id varchar(100) not null,
	quantity int not null,
	cost double(10, 2) not null,
	date_added date not null,
	primary key(cart_id, model_id),
	foreign key(cart_id) references ShoppingCart(cart_id) on DELETE cascade on UPDATE cascade,
	foreign key(model_id) references LaptopModel(model_id) on DELETE cascade on UPDATE cascade
);

/* Warehouse(warehouse_id, street, city, parish, telephone) */
create table Warehouse(
	warehouse_id int auto_increment not null,
	street varchar(100) not null,
	city varchar(100) not null,
	parish varchar(100) not null,
	telephone varchar(20) not null,
	primary key(warehouse_id)
);

/* WarehouseStock(warehouse_id, model_id, quantity) */
create table WarehouseStock(
	warehouse_id int not null,
	model_id varchar(100) not null,
	quantity int not null,
	primary key(warehouse_id, model_id),
	foreign key(warehouse_id) references Warehouse(warehouse_id) on DELETE cascade on UPDATE cascade,
	foreign key(model_id) references LaptopModel(model_id) on DELETE cascade on UPDATE cascade
);

/* Receipt(track_num, invoice) */
create table Receipt(
	track_num int not null,
	invoice blob not null,
	primary key(track_num)
);

/* Checkout(account_id, track_num, total_cost, transaction_date) */
create table Checkout(
	cart_id int not null,
	track_num int not null,
	total_cost double(20,2) not null,
	transaction_date date not null,
	primary key(cart_id, track_num),
	foreign key(cart_id) references ShoppingCart(cart_id) on DELETE cascade on UPDATE cascade,
	foreign key(track_num) references Receipt(track_num) on DELETE cascade on UPDATE cascade
);

/* PurchasedItems(product_id, model_id, account_id, branch_id, cost, date_purchased) */
create table PurchasedItems(
	purchase_id int auto_increment not null,
	product_id int not null,
	model_id varchar(100) not null,
	account_id int not null,
	branch_id varchar(50) not null,
	cost double(20,2) not null,
	date_purchased date not null,
	primary key(purchase_id),
	foreign key(model_id) references LaptopModel(model_id) on DELETE cascade on UPDATE cascade,
	foreign key(account_id) references CustomerCart(account_id) on DELETE cascade on UPDATE cascade,
	foreign key(branch_id) references Branch(branch_id) on DELETE cascade on UPDATE cascade
);

/* WriteReview(account_id, model_id, rev_text, date_written) */
create table WriteReview(
	account_id int not null,
	model_id varchar(100) not null,
	rev_text text not null,
	date_written date not null,
	primary key(account_id, model_id),
	foreign key(account_id) references CustomerAccount(account_id) on DELETE cascade on UPDATE cascade,
	foreign key(model_id) references LaptopModel(model_id) on DELETE cascade on UPDATE cascade
);


/*---------------------------PROCEDURE-------------------------------------------------------------------------------------------------------------*/

/*PROCEDURE for orderByPrice(argument varchar)*/ 
DELIMITER //
	CREATE PROCEDURE orderByPrice(IN ordr varchar(20))
	BEGIN
	IF ("ascending" like ordr) THEN SELECT * FROM LaptopModel order by price ASC;
	ELSE SELECT * FROM LaptopModel order by price DESC;
	END IF;
	END //
DELIMITER ;

/*PROCEDURE for getByModel(argument varchar)*/ 
DELIMITER //
	CREATE PROCEDURE getByModel(IN Model varchar(100))
	BEGIN
	SELECT * FROM LaptopModel WHERE lower(Model) LIKE CONCAT('%',Model,'%');
	END //
DELIMITER ;

/*PROCEDURE for getByBrand(argument varchar)*/ 
DELIMITER //
	CREATE PROCEDURE getByBrand(IN Brand varchar(100))
	BEGIN
	SELECT * FROM LaptopModel WHERE lower(brand) LIKE  CONCAT('%',Brand,'%');
	END //
DELIMITER ;

/*PROCEDURE for addPurchasedItem(argument int, argument int, argument varchar, argument double )*/ 
DELIMITER //
	CREATE PROCEDURE addPurchasedItem(IN product_id int, IN model_id varchar(100), IN account_id int, IN branch_id varchar(50), IN cost double(20,2))
	BEGIN
	INSERT INTO PurchasedItems VALUES (product_id, model_id, account_id, branch_id, old.cost, CURDATE());
	END //
DELIMITER ;

/*------------------------TRIGGER----------------------------------------------------------------------------------------------------------------------------*/

/* TRIGGER  newShoppingCart*/
DELIMITER $$
	CREATE TRIGGER newShoppingCart
	AFTER INSERT ON CustomerAccount
	FOR EACH ROW
	BEGIN
	INSERT INTO ShoppingCart VALUES (new.account_id,0,0.00);
	INSERT INTO CustomerCart VALUES (new.account_id,new.account_id);
	END $$
DELIMITER ;

/* TRIGGER  newCartItems*/
DELIMITER $$
	CREATE TRIGGER newCartItem
	AFTER INSERT ON CartItems
	FOR EACH ROW
	BEGIN
	UPDATE ShoppingCart SET item_count = item_count + new.quantity, value = value + new.cost WHERE cart_id = new.cart_id;
	END $$
DELIMITER ;

/* TRIGGER  UPDATECartItems*/
DELIMITER $$
	CREATE TRIGGER updateCartItem
	AFTER UPDATE ON CartItems
	FOR EACH ROW
	BEGIN
	UPDATE ShoppingCart SET item_count = ((item_count - old.quantity) + new.quantity), value = ((value - old.cost) + new.cost) WHERE cart_id = new.cart_id;
	END $$
DELIMITER ;

/* TRIGGER  DelectCartItems*/
DELIMITER $$
	CREATE TRIGGER deleteCartItem
	AFTER DELETE ON CartItems
	FOR EACH ROW
	BEGIN
	UPDATE ShoppingCart SET item_count = (item_count - old.quantity), value = (value - old.cost) WHERE cart_id = old.cart_id;
	END $$
DELIMITER ;


/*======================= Branch1 Database ===================================================*/

create database Branch1;
use Branch1;

/* LaptopModel(model_id, model, brand, cpu_specs, display_size, resolution, operating_system, gpu_specs, launch_date, thumbnail) */
create table LaptopModel(
	model_id varchar(100) not null,
	model text not null,
	brand varchar(100) not null,
	cpu_specs text, 
	display_size double(5,2), 
	resolution varchar(100),
	operating_system text,
	gpu_specs text,
	launch_date date,
	thumbnail text,
	primary key(model_id) 
);

/* ModelStockInfo(model_id, amt_in_stock, amt_sold) */
create table ModelStockInfo(
	model_id varchar(100)not null ,
	amt_in_stock int not null,
	primary key(model_id),
	foreign key(model_id) references LaptopModel(model_id) on DELETE cascade on UPDATE cascade
);

/* ModelItem(product_id, model_id) */
create table ModelItem(
	model_id varchar(100) not null,
	product_id int not null,
	primary key(model_id, product_id),
	foreign key(model_id) references LaptopModel(model_id) on DELETE cascade on UPDATE cascade
);

/*------PROCEDURE-------------------------------------------------------------------------------------------------------*/
/*CREATE FUNCTION getProducts(@modelId varchar(100), @amt int)
RETURNS TABLE AS
RETURN (SELECT product_id FROM   ModelItem WHERE  model_id = @modelId LIMIT @amt)*/

/*PROCEDURE for purchaseItem(argument varchar,argument int))*/  
DELIMITER //
	CREATE PROCEDURE purchaseItem(IN modelId varchar(100), OUT prod_id INT)
	BEGIN
	UPDATE ModelStockInfo SET amt_in_stock = (amt_in_stock - 1) WHERE model_id like modelId;
	
	SELECT product_id into prod_id FROM ItemsInStock where model_id like modelId LIMIT 1;
	DELETE FROM ItemsInStock WHERE product_id like prod_id;
	END //
DELIMITER ;


/*======================= Branch2 Database ===================================================*/

create database Branch2;
use Branch2;

/* LaptopModel(model_id, model, brand, cpu_specs, display_size, resolution, operating_system, gpu_specs, launch_date, thumbnail) */
create table LaptopModel(
	model_id varchar(100) not null,
	model text not null,
	brand varchar(100) not null,
	cpu_specs text, 
	display_size double(5,2), 
	resolution varchar(100),
	operating_system text,
	gpu_specs text,
	launch_date date,
	thumbnail text,
	primary key(model_id) 
);

/* ModelStockInfo(model_id, amt_in_stock, amt_sold) */
create table ModelStockInfo(
	model_id varchar(100)not null ,
	amt_in_stock int not null,
	primary key(model_id),
	foreign key(model_id) references LaptopModel(model_id) on DELETE cascade on UPDATE cascade
);

/* ModelItem(product_id, model_id) */
create table ModelItem(
	model_id varchar(100) not null,
	product_id int not null,
	primary key(model_id, product_id),
	foreign key(model_id) references LaptopModel(model_id) on DELETE cascade on UPDATE cascade
);

/*------PROCEDURE-------------------------------------------------------------------------------------------------------*/
/*CREATE FUNCTION getProducts(@modelId varchar(100), @amt int)
RETURNS TABLE AS
RETURN (SELECT product_id FROM   ModelItem WHERE  model_id = @modelId LIMIT @amt)*/

/*PROCEDURE for purchaseItem(argument varchar,argument int))*/  
DELIMITER //
	CREATE PROCEDURE purchaseItem(IN modelId varchar(100), OUT prod_id INT)
	BEGIN
	UPDATE ModelStockInfo SET amt_in_stock = (amt_in_stock - 1) WHERE model_id like modelId;
	
	SELECT product_id into prod_id FROM ItemsInStock where model_id like modelId LIMIT 1;
	DELETE FROM ItemsInStock WHERE product_id like prod_id;
	END //
DELIMITER ;


/*======================= Branch3 Database ===================================================*/

create database Branch3;
use Branch3;

/*LaptopModel(model_id, model, brand, cpu_specs, display_size, resolution, operating_system, gpu_specs, launch_date, thumbnail)*/
create table LaptopModel(
	model_id varchar(100) not null,
	model text not null,
	brand varchar(100) not null,
	cpu_specs text, 
	display_size double(5,2), 
	resolution varchar(100),
	operating_system text,
	gpu_specs text,
	launch_date date,
	thumbnail text,
	primary key(model_id) 
);

/* ModelStockInfo(model_id, amt_in_stock, amt_sold) */
create table ModelStockInfo(
	model_id varchar(100)not null ,
	amt_in_stock int not null,
	primary key(model_id),
	foreign key(model_id) references LaptopModel(model_id) on DELETE cascade on UPDATE cascade
);

/* ModelItem(product_id, model_id) */
create table ModelItem(
	model_id varchar(100) not null,
	product_id int not null,
	primary key(model_id, product_id),
	foreign key(model_id) references LaptopModel(model_id) on DELETE cascade on UPDATE cascade
);

/*------PROCEDURE-------------------------------------------------------------------------------------------------------*/
/*CREATE FUNCTION getProducts(@modelId varchar(100), @amt int)
RETURNS TABLE AS
RETURN (SELECT product_id FROM   ModelItem WHERE  model_id = @modelId LIMIT @amt)*/

/*PROCEDURE for purchaseItem(argument varchar,argument int))*/  
DELIMITER //
	CREATE PROCEDURE purchaseItem(IN modelId varchar(100), OUT prod_id INT)
	BEGIN
	UPDATE ModelStockInfo SET amt_in_stock = (amt_in_stock - 1) WHERE model_id like modelId;
	
	SELECT product_id into prod_id FROM ItemsInStock where model_id like modelId LIMIT 1;
	DELETE FROM ItemsInStock WHERE product_id like prod_id;
	END //
DELIMITER ;


/*======================= MultlinkBankinformation Database ===================================================*/

create database MultiLink;
use MultiLink;

/* CreditCardDetails(card_num, name_on_card, card_security_code, expiration_month, expiration_year, billing_street, billing_city, billing_parish) */
create table BankCreditCardDetails(
	card_num int not null,
	name_on_card varchar(100),
	card_security_code int,
	expiration_month varchar(10) not null,
	expiration_year varchar(10) not null,
	billing_street varchar(100) not null,
	billing_city varchar(100) not null,
	billing_parish varchar(100) not null,
	primary key(card_num) 
);

/* view provided by a bank's database to check if the customer's credit card exists and if he/she can make this purchase. */
CREATE VIEW BanksCreditCards AS SELECT * FROM BankCreditCardDetails;

/* CustomerAccount(account_id, email, password, fname, lname, gender, date_of_birth, street, city, parish, telephone, open_on)
create table CustomerAcc(
	account_id int auto_increment not null,
	email varchar(100),
	password varchar(255) not null,
	fname varchar(30) not null,
	lname varchar(30) not null,
	gender varchar(20) not null,
	date_of_birth Date not null,
	street varchar(100)not null,
	city varchar(100) not null,
	parish varchar(100) not null,
	telephone varchar(20),
	open_on Date not null,
	primary key(account_id) 
);*/

/* bank(bank_id, bank_name, account_id,account_balance)
create table Bank(
	bank_id int auto_increment not null,
	bank_name varchar(100) not  null,
	account_id	int not null,
	account_balance decimal(10,2) not null,
	primary key(bank_id,account_id),
	foreign key(account_id) references CustomerAcc(account_id) on DELETE cascade on UPDATE cascade
);*/

/*CustomerCreditCard(account_id, card_num)
create table CustCreditCard(
	account_id int not null,
	card_num int not null,
	primary key(account_id, card_num),
	foreign key(account_id) references CustomerAcc(account_id) on DELETE cascade on UPDATE cascade,
	foreign key(card_num) references CreditCardDetail(card_num) on DELETE cascade on UPDATE cascade
);
*/

use CompuStore;