import io
import qrcode
import pyodbc

def make_qr_png_bytes(payload: str, box_size=10, border=2) -> bytes:
    qr = qrcode.QRCode(
        version=None,
        error_correction=qrcode.constants.ERROR_CORRECT_M,
        box_size=box_size,
        border=border,
    )
    qr.add_data(payload)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white").convert("RGB")

    buf = io.BytesIO()
    img.save(buf, format="PNG")
    return buf.getvalue()

def save_ticket_qr(ticket_id: str, png_bytes: bytes):
    cnxn = pyodbc.connect("Driver={ODBC Driver 18 for SQL Server};"
                    r"Server=LAP-25-I01\SQLEXPRESS;"
                    "Database=FestivalCateringAPP;"
                    "Trusted_Connection=yes;"
                    "Encrypt=yes;"
                    "TrustServerCertificate=yes;")

    cur = cnxn.cursor()
    cur.execute(
        "UPDATE Tickets SET QrPng = ? WHERE TicketNR = ?",
        (pyodbc.Binary(png_bytes), ticket_id)
    )
    cnxn.commit()

qr_code = make_qr_png_bytes("TicketNR = 8910111")
save_ticket_qr(8910111, qr_code)