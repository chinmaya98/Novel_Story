import qrcode

# The link to your deployed application
app_link = "https://happybirthdaygautam.streamlit.app/"

# Generate the QR code
img = qrcode.make(app_link)

# Save the file to your desktop folder
img.save("Gautam_App_QR.png")

print("Success! Your QR code is saved as Gautam_App_QR.png")