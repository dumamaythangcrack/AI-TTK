export default async function handler(req, res) {
  const { prompt } = await req.json();
  const key = process.env.GEMINI_API_KEY;

  const result = await fetch(
    `https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash-latest:generateContent?key=${key}`,
    {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        contents: [{ parts: [{ text: prompt }] }]
      }),
    }
  );

  const data = await result.json();
  res.status(200).json({ reply: data.candidates?.[0]?.content?.parts?.[0]?.text || "..." });
}
