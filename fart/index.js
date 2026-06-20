const { Client } = require('discord.js-selfbot-v13');
const { VoiceConnection } = require('discord-video-stream');
const config = require('./config.json');

const client = new Client();

client.on('ready', () => {
    console.log(`[INFO] Akun berhasil login sebagai ${client.user.tag}!`);
});

client.on('messageCreate', async (message) => {
    // Keamanan: Hanya jalankan jika perintah dari user yang diizinkan
    if (!config.acceptedAuthors.includes(message.author.id)) return;

    if (message.content.startsWith('!join')) {
        const channel = message.member.voice.channel;
        if (!channel) return message.reply('❌ Anda harus masuk ke voice channel terlebih dahulu!');

        try {
            // Auto Join Voice Channel
            const connection = new VoiceConnection(channel);
            connection.on('ready', () => {
                message.reply('🔊 Berhasil bergabung ke Voice Channel!');
            });
            // Simpan connection di client agar bisa digunakan untuk Go Live
            client.voiceConnection = connection;
        } catch (error) {
            console.error(error);
            message.reply('❌ Gagal bergabung ke channel.');
        }
    }

    if (message.content.startsWith('!play-live')) {
        const args = message.content.split(' ');
        const videoLink = args[1];

        if (!videoLink) return message.reply('❌ Tolong sertakan link video (contoh: !play-live <link_mp4>)');
        if (!client.voiceConnection) return message.reply('❌ Gunakan perintah !join terlebih dahulu!');

        try {
            // Memulai proses Go Live (Stream) dan membuka link
            // Link yang dimasukkan harus direct video stream (seperti .mp4 atau link HLS)
            await client.voiceConnection.play(videoLink);
            message.reply('🎥 Sedang membuka link & Go Live seperti bioskop!');
        } catch (error) {
            console.error(error);
            message.reply('❌ Gagal memulai Go Live.');
        }
    }
});

client.login(config.token);
          
