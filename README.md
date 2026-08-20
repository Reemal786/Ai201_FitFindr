# 👕 ThriftFit — AI-Powered Secondhand Fashion Assistant

**ThriftFit** is an AI-powered fashion assistant that helps users discover secondhand clothing and figure out how to style new pieces with items they already own.

Users describe what they're looking for, including their **style, size, and budget**, and ThriftFit searches available secondhand listings, selects a relevant item, and generates a personalized outfit using the user's existing wardrobe.

The application uses an **agent-based workflow** to coordinate search, outfit generation, and creation of a shareable **Fit Card**.

## 🎯 Purpose

Finding secondhand clothing is only part of building an outfit. It can also be difficult to determine whether a new piece works with clothes you already own.

ThriftFit combines **secondhand discovery and AI-powered styling** into one workflow, helping users find affordable pieces while making better use of their existing wardrobe.

The project also explores how **LLMs, tool calling, state management, and agent workflows** can be combined to build an AI application that completes a multi-step task rather than generating a single response.

## ✨ Features

* **Natural Language Search** — Describe the clothing item you're looking for conversationally
* **Budget & Size Filtering** — Find listings that match specified size and price requirements
* **Secondhand Item Discovery** — Search a dataset of secondhand clothing listings
* **AI Outfit Recommendations** — Generate outfits combining newly discovered pieces with clothes already in your wardrobe
* **Personalized Styling** — Outfit recommendations account for the selected item's color, category, and style
* **Fit Cards** — Generate short, shareable descriptions of completed outfits
* **Agent-Based Workflow** — Coordinates multiple specialized tools to complete a user's request
* **Error Handling** — Provides alternatives when listings aren't available or wardrobe information is missing

## 🤖 How ThriftFit Works

ThriftFit uses three specialized tools that work together:

### 1. `search_listings`

Searches secondhand listings using the user's:

* Item description
* Size
* Maximum price

Matching listings are ranked based on their relevance to the user's request.

### 2. `suggest_outfit`

Takes the selected secondhand item and combines it with pieces from the user's existing wardrobe.

An LLM generates a complete outfit recommendation and explains how the pieces work together.

### 3. `create_fit_card`

Transforms the final outfit into a short, shareable caption describing the thrifted item and completed look.

## 🧠 Agent Architecture

```text
                User Request
                     │
                     ▼
          Extract Search Criteria
          ┌──────────┼──────────┐
          ▼          ▼          ▼
     Description    Size      Budget
          │          │          │
          └──────────┼──────────┘
                     ▼
              search_listings
                     │
                     ▼
              Matching Items
                     │
                     ▼
             Select Best Match
                     │
                     ▼
              suggest_outfit
                     │
            ┌────────┴────────┐
            ▼                 ▼
      Selected Item      User Wardrobe
            │                 │
            └────────┬────────┘
                     ▼
             Outfit Suggestion
                     │
                     ▼
              create_fit_card
                     │
                     ▼
        Item + Outfit + Fit Card
```

The agent maintains a session containing the user's query, search criteria, search results, selected item, wardrobe, outfit suggestion, and final Fit Card as information moves between tools.

## 🛠️ Tech Stack

**Language**

* Python

**AI**

* Llama 3.3 70B
* Groq API
* LLM Tool Calling
* Agent-Based Workflows

**Interface**

* Gradio

**Data**

* JSON
* Mock secondhand clothing dataset

## 🔄 Example

### User Request

> I'm looking for a vintage graphic tee under $30. I mostly wear baggy jeans and chunky sneakers. What's out there and how would I style it?

### ThriftFit Workflow

**1. Search**

ThriftFit extracts:

```text
Item: Vintage graphic tee
Budget: $30
```

It then searches the available secondhand listings.

**2. Select**

A matching item could be:

```text
Faded Band Tee
Price: $22
Platform: Depop
Condition: Good
```

**3. Style**

ThriftFit combines the new item with pieces from the user's wardrobe:

```text
Faded Band Tee
+ Baggy Jeans
+ Chunky Sneakers
```

The AI then explains how the pieces work together to create a vintage streetwear look.

**4. Create Fit Card**

Finally, ThriftFit generates a short shareable caption for the completed outfit.

## 🧩 State Management

ThriftFit maintains a session throughout the agent workflow so information can move between tools without requiring the user to repeatedly provide it.

The session tracks:

```text
user_query
description
size
max_price
search_results
selected_item
wardrobe
outfit_suggestion
fit_card
error
```

Each tool's output becomes input for the next stage of the workflow.

## 🛡️ Error Handling

ThriftFit is designed to handle incomplete or unsuccessful requests without breaking the workflow.

If no listings match the user's request, the agent suggests:

* Increasing the budget
* Removing the size restriction
* Using a broader description

If wardrobe information isn't available, ThriftFit can still provide general styling recommendations based on the selected item.

## 🔮 Future Improvements

* Connect to live secondhand marketplaces
* Allow users to upload and manage their own digital wardrobe
* Add image-based clothing recognition
* Support additional filters such as brand, color, and condition
* Add favorite and saved outfits
* Track previously generated outfits
* Provide multiple outfit recommendations for each item
* Add personalized style profiles

## 👩‍💻 Author

**Reemal Hoor**
Computer Engineering
