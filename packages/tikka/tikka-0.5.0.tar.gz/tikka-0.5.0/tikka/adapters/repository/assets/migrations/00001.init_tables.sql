create table if not exists currency(
    code_name varchar(255) unique primary key not null,
    name varchar(255),
    ss58_format integer,
    token_decimals integer default null,
    token_symbol varchar(255) default null,
    universal_dividend integer default null,
    monetary_mass integer default null,
    members_count integer default null
);

create table if not exists accounts(
        address varchar(255) unique primary key not null,
        uid varchar(255),
        crypto_type integer default null,
        balance integer default null
);

create table if not exists wallets(
        address varchar(255) unique primary key not null,
        encrypted_seed varchar(65535),
        encryption_nonce varchar(255),
        encryption_mac_tag varchar(255)

);

create table if not exists tabs(
        id varchar(255) unique primary key not null,
        panel_class varchar(255) not null
);

create table if not exists preferences(
        key_ varchar(255) unique primary key not null,
        value_ varchar(65535)
);

-- PREFERENCES FIELDS
INSERT INTO preferences (key_, value_) VALUES ("selected_tab_page", NULL);
INSERT INTO preferences (key_, value_) VALUES ("wallet_load_default_directory", null);
INSERT INTO preferences (key_, value_) VALUES ("wallet_save_default_directory", null);
INSERT INTO preferences (key_, value_) VALUES ("current_entry_point_url", null);
INSERT INTO preferences (key_, value_) VALUES ("selected_unit", "unit");

create table entry_points (
        url varchar(255) primary key not null,
        node_id varchar(255),
        FOREIGN KEY(node_id) REFERENCES nodes(id)
);

create table nodes (
        id varchar(255) primary key not null,
        peer_id varchar(255),
        block integer,
        software varchar(255),
        software_version varchar(255)
);
