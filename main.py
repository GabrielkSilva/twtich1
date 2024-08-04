import logging
from flask import Flask
from colorama import Fore
from TwitchChannelPointsMiner import TwitchChannelPointsMiner
from TwitchChannelPointsMiner.logger import LoggerSettings, ColorPalette
from TwitchChannelPointsMiner.classes.Chat import ChatPresence
from TwitchChannelPointsMiner.classes.Discord import Discord
from TwitchChannelPointsMiner.classes.Webhook import Webhook
from TwitchChannelPointsMiner.classes.Telegram import Telegram
from TwitchChannelPointsMiner.classes.Matrix import Matrix
from TwitchChannelPointsMiner.classes.Pushover import Pushover
from TwitchChannelPointsMiner.classes.Settings import Priority, Events, FollowersOrder
from TwitchChannelPointsMiner.classes.entities.Bet import Strategy, BetSettings, Condition, OutcomeKeys, FilterCondition, DelayMode
from TwitchChannelPointsMiner.classes.entities.Streamer import Streamer, StreamerSettings

# Inicialize o Flask
app = Flask(__name__)

@app.route('/')
def home():
    return "Twitch Channel Points Miner is running!"

# Configuração do Twitch Channel Points Miner
twitch_miner = TwitchChannelPointsMiner(
    username="pingtvk",
    password="27995767*",
    claim_drops_startup=False,
    priority=[
        Priority.STREAK,
        Priority.DROPS,
        Priority.ORDER
    ],
    enable_analytics=False,
    disable_ssl_cert_verification=False,
    disable_at_in_nickname=False,
    logger_settings=LoggerSettings(
        save=True,
        console_level=logging.INFO,
        console_username=False,
        auto_clear=True,
        time_zone="",
        file_level=logging.DEBUG,
        emoji=True,
        less=False,
        colored=True,
        color_palette=ColorPalette(
            STREAMER_online="GREEN",
            streamer_offline="red",
            BET_wiN=Fore.MAGENTA
        ),
        telegram=Telegram(
            chat_id=123456789,
            token="123456789:shfuihreuifheuifhiu34578347",
            events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE,
                    Events.BET_LOSE, Events.CHAT_MENTION],
            disable_notification=True,
        ),
        discord=Discord(
            webhook_api="https://discord.com/api/webhooks/1269664021536178186/Rc9sddx-hEQu_6AHv7Ygg3OP_4J4fV6WsXxbMYVcxz3XpBsQKZ00zg8UbWedvPa7thIU",
            events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE,
                    Events.BET_LOSE, Events.CHAT_MENTION],
        ),
        webhook=Webhook(
            endpoint="https://example.com/webhook",
            method="GET",
            events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE,
                    Events.BET_LOSE, Events.CHAT_MENTION],
        ),
        matrix=Matrix(
            username="twitch_miner",
            password="...",
            homeserver="matrix.org",
            room_id="...",
            events=[Events.STREAMER_ONLINE, Events.STREAMER_OFFLINE, Events.BET_LOSE],
        ),
        pushover=Pushover(
            userkey="YOUR-ACCOUNT-TOKEN",
            token="YOUR-APPLICATION-TOKEN",
            priority=0,
            sound="pushover",
            events=[Events.CHAT_MENTION, Events.DROP_CLAIM],
        )
    ),
    streamer_settings=StreamerSettings(
        make_predictions=True,
        follow_raid=True,
        claim_drops=True,
        claim_moments=True,
        watch_streak=True,
        chat=ChatPresence.ONLINE,
        bet=BetSettings(
            strategy=Strategy.SMART,
            percentage=5,
            percentage_gap=20,
            max_points=50000,
            stealth_mode=True,
            delay_mode=DelayMode.FROM_END,
            delay=6,
            minimum_points=20000,
            filter_condition=FilterCondition(
                by=OutcomeKeys.TOTAL_USERS,
                where=Condition.LTE,
                value=800
            )
        )
    )
)

# Adicione os streamers
twitch_miner.mine(
    [
        Streamer("miratortatv", settings=StreamerSettings(make_predictions=True, follow_raid=False, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=True, percentage_gap=20, max_points=234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_USERS, where=Condition.LTE, value=800)))),
        Streamer("Majorz1", settings=StreamerSettings(make_predictions=False, follow_raid=True, claim_drops=False, bet=BetSettings(strategy=Strategy.PERCENTAGE, percentage=5, stealth_mode=False, percentage_gap=20, max_points=1234, filter_condition=FilterCondition(by=OutcomeKeys.TOTAL_POINTS, where=Condition.GTE, value=250)))),
        Streamer("AfricaAlbion", settings=StreamerSettings(make_predictions=True, follow_raid=False, watch_streak=True, bet=BetSettings(strategy=Strategy.SMART, percentage=5, stealth_mode=False, percentage_gap=30, max_points=50000, filter_condition=FilterCondition(by=OutcomeKeys.ODDS, where=Condition.LT, value=300)))),
        Streamer("Gu4rdaTv", settings=StreamerSettings(make_predictions=False, follow_raid=True, watch_streak=True)),
        Streamer("jovemexp", settings=StreamerSettings(make_predictions=True, follow_raid=True, claim_drops=True, watch_streak=True, bet=BetSettings(strategy=Strategy.HIGH_ODDS, percentage=7, stealth_mode=True, percentage_gap=20, max_points=90, filter_condition=FilterCondition(by=OutcomeKeys.PERCENTAGE_USERS, where=Condition.GTE, value=300)))),
        Streamer("jamesrenascido"),
        Streamer("nemezizyt"),
        Streamer("Kinntaroo"),
        "Umiiie",
        "Murloka",
        "BlytheOnee",
        "Feliperas"
    ],
    followers=False,
    followers_order=FollowersOrder.ASC
)

# Execute o servidor Flask na porta especificada
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
