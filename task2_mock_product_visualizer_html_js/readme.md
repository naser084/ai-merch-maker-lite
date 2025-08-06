#  Task 2: Mock Product Visualizer

A simple browser-based tool that allows you to **upload any design/logo** and overlay it on a **t-shirt template** to simulate a product mockup.

 Built as part of the **AI Developer Internship Assignment** at **Smart Ecom Tech**.

---

## 🔧 Features

-  Upload any image (like a logo, graphic, or design)
-  Automatically overlays your image on a **t-shirt template**
-  Generates a **mock JSON response** similar to **Printful API** output
-  Runs locally — no server or installation needed

---

##  How to Run It

>  **No server or coding tool needed**

1. Open the folder named `visualizer/`
2. Double-click `index.html`
3. The app opens in your browser
4. Upload any image (`.png`, `.jpg`, etc.)
5. You'll see:
   - Your uploaded image placed on a t-shirt
   - A **mock JSON response** generated below

---

##  Example Use Case

- Upload: `logo.png`
- T-shirt Preview: Shows your logo on a t-shirt image
- JSON Output:
```json
{
  "mockup_id": "mock123",
  "product": "tshirt",
  "image_url": "your_uploaded_image.png",
  "template_url": "tshirt_template.png",
  "final_mockup_url": "generated_mockup.png"
}
