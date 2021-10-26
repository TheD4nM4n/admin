module.exports = {
    name: 'ready',
    once: true,
    execute(client) {
        console.log(`Successfully logged in as ${client.user.username}.`);
    }
}