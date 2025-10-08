from macpymessenger import Configuration, IMessageClient

configuration = Configuration()
client = IMessageClient(configuration)

client.create_template("welcome", "Hello, {{ name }}! Welcome aboard.")
client.send_template("+18153239580", "welcome", {"name": "Ethan"})