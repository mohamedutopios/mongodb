Parfait 👍
Voici **LA solution officielle et propre** pour avoir **un client MongoDB en ligne de commande** sur **macOS** **et** **Windows**, avec les **commandes exactes** et sans bricolage.

---

# 🎯 Client CLI officiel : **mongosh**

> `mongosh` = **MongoDB Shell moderne** (remplace `mongo`)

---

## 🍎 macOS (Intel & Apple Silicon)

### 1️⃣ Installation (Homebrew)

```bash
brew tap mongodb/brew
brew install mongodb-community-shell
```

### 2️⃣ Vérifier

```bash
mongosh --version
```

### 3️⃣ Connexion à TON Mongo Docker

```bash
mongosh "mongodb://admin:password@localhost:27017/?authSource=admin"
```

---

## 🪟 Windows (Windows 10 / 11)

### 🔹 Méthode 1 — Installateur officiel (recommandée)

1. Télécharge **MongoDB Shell** :
   👉 [https://www.mongodb.com/try/download/shell](https://www.mongodb.com/try/download/shell)
2. Choisis :

   * OS : **Windows**
   * Package : **msi**
3. Installe (cocher **Add to PATH**)

### Vérifier

```powershell
mongosh --version
```

### Connexion

```powershell
mongosh "mongodb://admin:password@localhost:27017/?authSource=admin"
```

---

### 🔹 Méthode 2 — Chocolatey

```powershell
choco install mongosh
```

---

## 🧪 Tests rapides (communs Mac & Windows)

```js
show dbs
use microservices_answers_db
db.test.insertOne({ os: "mac/windows", ok: true })
db.test.find()
```

---

## ⚠️ Points importants (90 % des erreurs)

### 🔐 `authSource` obligatoire

❌ Sans :

```text
Authentication failed
```

✅ Toujours :

```text
?authSource=admin
```

---

### 🐳 Docker

| Où tu es         | Host        |
| ---------------- | ----------- |
| Mac / Windows    | `localhost` |
| Conteneur Docker | `mongodb`   |

---

## 🧠 Résumé clair

| OS      | Installation                           | Connexion               |
| ------- | -------------------------------------- | ----------------------- |
| macOS   | `brew install mongodb-community-shell` | `mongosh mongodb://...` |
| Windows | MSI ou Chocolatey                      | `mongosh mongodb://...` |
| Docker  | `docker exec ... mongosh`              | localhost ou mongodb    |

---

## 🔐 Bonus (facultatif)

### Alias pratique

```bash
alias mongo-docker='mongosh "mongodb://admin:password@localhost:27017/?authSource=admin"'
```

---

Si tu veux :

* scripts d’init `.js`
* connexion Spring Boot
* réplica set Mongo
* lab sécurité Mongo (auth / brute force)

Dis-moi 👌
