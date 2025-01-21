from flask import Flask, request, jsonify
import requests  # 바이낸스 API 또는 외부 API를 위한 라이브러리

app = Flask(__name__)

# 바이낸스 API 키 및 시크릿 (예시로 추가, 실제 키로 교체 필요)
BINANCE_API_KEY = "wuhPFDsVhuQWiCeuqUpuRo9IdsFcwtAm2vvwnbwmm6sfUo52aVyrghKMcPIRn6GS"
BINANCE_API_SECRET = "3OUunsf5cLbE4AEm43e6SuMArHRW3IAux8Bo29ytnO22hCP3Vq76bffYfLo0VVHU"

def place_order(order_type, symbol, usdt_amount):
    # 바이낸스 가격 데이터 가져오기
    price_url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}"
    price_response = requests.get(price_url)
    price = float(price_response.json()["price"])

    # BTC 수량 계산 (USDT / 현재 가격)
    quantity = usdt_amount / price

    # 주문 요청
    url = "https://api.binance.com/api/v3/order"
    headers = {
        "X-MBX-APIKEY": BINANCE_API_KEY
    }
    payload = {
        "symbol": symbol,
        "side": "BUY" if order_type == "buy" else "SELL",
        "type": "MARKET",
        "quantity": round(quantity, 6),  # 소수점 6자리로 제한
    }
    response = requests.post(url, headers=headers, data=payload)
    print("바이낸스 API 응답:", response.json())
    return response.json()

@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.json
    print("Received data:", data)

    # TradingView에서 보내는 alert_message를 처리
    alert_message = data.get("alert_message", "")

    if alert_message == "롱 포지션 진입":
        print("롱 포지션 진입!")
        # 바이낸스 API로 매수 요청
        response = place_order("buy", "BTCUSDT", 0.001)
        print("롱 포지션 진입 응답:", response)  # 추가 출력
    elif alert_message == "숏 포지션 진입":
        print("숏 포지션 진입!")
        # 바이낸스 API로 매도 요청
        response = place_order("sell", "BTCUSDT", 0.001)
        print("숏 포지션 진입 응답:", response)  # 추가 출력
    elif alert_message == "롱 청산":
        print("롱 포지션 청산!")
        # 롱 청산 로직
    elif alert_message == "숏 청산":
        print("숏 포지션 청산!")
        # 숏 청산 로직
    else:
        print("알 수 없는 메시지:", alert_message)

    return jsonify({"status": "success"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
