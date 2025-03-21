import flet as ft
import yfinance as yf

def main(page: ft.Page):
    page.title = "Flet Stock App"
    page.vertical_alignment = ft.MainAxisAlignment.CENTER
    page.horizontal_alignment = ft.CrossAxisAlignment.CENTER

    def get_stock_data(e):
        symbol = stock_symbol.value.strip().upper()
        try:
            data = yf.Ticker(symbol).history(period="1y")
            if not data.empty:  # Check if data is not empty
                result.value = f"Latest Price for {symbol}: {data.iloc[-1].Close}"
            else:
                result.value = f"No data available for {symbol}. Check the symbol or try later."
            stock_symbol.value = ""
        except Exception as ex:
            result.value = f"Error: {ex}"
            stock_symbol.value = ""
        page.update()

    stock_symbol = ft.TextField(label="Enter Stock Symbol", width=200)
    result = ft.Text()
    fetch_button = ft.ElevatedButton(text="Fetch", on_click=get_stock_data)

    page.add(ft.Column([stock_symbol, fetch_button, result], horizontal_alignment=ft.CrossAxisAlignment.CENTER))

ft.app(target=main)
