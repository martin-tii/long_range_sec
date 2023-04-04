use p256::{EncodedPoint, PublicKey, ecdh::EphemeralSecret};
use rand_core::OsRng;
use std::io::{self, Read, Write};
use std::net::{TcpListener, TcpStream};
use config::{Config, ConfigError, File};

fn exchange_public_keys(stream: &mut TcpStream) -> io::Result<Vec<u8>> {
    let secret = EphemeralSecret::random(&mut OsRng);
    let pk_bytes = EncodedPoint::from(secret.public_key());
    println!("my pub key: {:?}", pk_bytes.as_ref());

    stream.write_all(pk_bytes.as_ref())?;
    let mut buf = [0u8; 65];
    stream.read_exact(&mut buf)?;
    println!("look: {:?}", &buf);
    let their_pk = PublicKey::from_sec1_bytes(&buf)
        .expect("failed to parse received public key");
    let shared_secret = secret.diffie_hellman(&their_pk);
    Ok(shared_secret.raw_secret_bytes().to_vec())
}

fn start_server(config: &Config) -> io::Result<()> {
    let listener = TcpListener::bind(config.get_string("ip").unwrap())?;
    for stream in listener.incoming() {
        let mut stream = stream?;
        let shared_secret = exchange_public_keys(&mut stream)?;
        println!("Server received shared secret: {:x?}", hex::encode(&shared_secret));
        std::fs::write("shared_secret.txt", hex::encode(&shared_secret))?;
    }
    Ok(())
}

fn start_client(config: &Config) -> io::Result<()> {
    let mut stream = TcpStream::connect(config.get_string("ip").unwrap())?;
    let shared_secret = exchange_public_keys(&mut stream)?;
    println!("Client received shared secret: {:x?}", hex::encode(&shared_secret));
    std::fs::write("shared_secret.txt", hex::encode(&shared_secret))?;
    Ok(())
}

fn main() -> io::Result<()> {
    let mut config = Config::default();
    config.merge(File::with_name("config.toml")).unwrap();

    match std::env::args().nth(1) {
        Some(arg) if arg == "client" => start_client(&config),
        Some(arg) if arg == "server" => start_server(&config),
        _ => {
            eprintln!("Invalid mode. Usage: ./program [client|server]");
            Ok(())
        }
    }
}