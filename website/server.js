import express from "express";
import path from "path";
import { fileURLToPath } from "url";
import nunjucks from "nunjucks";

const __filename = fileURLToPath(import.meta.url);
const __dirname = path.dirname(__filename);

const app = express();
app.use(express.urlencoded({ extended: true }));
app.use(express.static(path.join(__dirname, "public")));

nunjucks.configure(path.join(__dirname, "views"), {
    autoescape: true,
    express: app,
    watch: true,
});

app.get("/", (req, res) => {
    res.render("index.html", { title: "Home Page" });
});

app.get("/login", (req, res) => {
    res.render("login.html")
})

app.post("/auth", (req, res) => {
    const { username, password } = req.body;
})

app.listen(3000, () => {
    console.log("Server started at http://localhost:3000")
})

