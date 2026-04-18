---
layout: post
title: "Three ways to store a note. I picked the wrong one first."
date: 2026-04-18
description: "How I deleted 340 lines of code by replacing a typed block model with a plain markdown string — and what the trap is worth naming."
tags: software-design, refactoring, tayis, notes, simplicity
---

I just deleted ~340 lines of code from a single file. The whole change touched 19 files and was *net negative 58 lines of code* — and that's only because I added a 402-line one-shot migration script along the way. Strip the migration script out, and I removed about 460 lines of code from the running system.

What did I delete? An entire data representation. My notes app, Tayis, used to store notes as a typed array of blocks:

```ts
type Block = {
  id: string
  type: "text" | "heading1" | "heading2" | "heading3"
       | "bullet_list" | "numbered_list" | "checkbox"
       | "quote" | "code" | "image" | "divider"
  content: string
  attributes?: Record<string, unknown>
  order: number
}

type Note = { id: string; title: string; blocks: Block[]; ... }
```

Now it stores them like this:

```ts
type Note = { id: string; title: string; content: string; ... }
```

`content` is just a markdown string. That's it. 3,347 existing notes converted in a few seconds. Nothing about the user-facing experience changed. Everything underneath got dramatically simpler.

This post is about how I ended up with the block model in the first place, what its hidden costs were, and why I think this trap is worth naming.

## Why blocks seemed reasonable

I didn't pick the block model because I thought it was clever. At the time I was building the editor, I was using Tiptap — a rich-text editor framework that models documents as a tree of typed nodes. Tiptap's internal representation is structured. It felt natural to persist that structure. Notion had popularised the block paradigm. Every note app seemed to be going that direction. And there was a vague sense that keeping the data structured would make future features easier: maybe I'd want to query "all checkbox blocks across all notes", or render notes differently depending on block type, or support block-level permissions someday.

None of those features ever materialised. What did materialise was friction — in every single place that needed to read a note.

## The hidden costs

The block model looked clean at the schema level. In practice it created a translation problem everywhere downstream.

The agent tool — the part of Tayis that lets an AI assistant read and write notes — had to reconstruct a readable string from the block array every time it wanted to do anything with a note's content. That meant a `blocksToMarkdown` function that had to handle every block type, stay in sync with the editor's rendering logic, and be tested separately.

Search indexing had the same problem. So did the sharing view. So did the insights feature. So did auto-tagging. So did list previews. Every consumer of note content was paying the same translation tax, independently.

The editor — the one producer — was the only thing that actually benefited from the block structure. And even there, Tiptap can render from a markdown string just as well as from a node tree. The structure wasn't load-bearing for the editor either.

Meanwhile, the block model had its own consistency problems. `content` inside a block was still a string. Inline formatting — bold, italic, links — lived inside that string as markdown conventions, not as structured data. So the representation was simultaneously over-engineered (typed block array) and under-engineered (unstructured inline content). It had the costs of structure without the benefits.

## The migration

Once I decided to make the switch, the path was straightforward. Write a `blocksToMarkdown` function (I already had one, for the agent tool). Run it over all 3,347 notes. Swap the schema. Delete the block-handling code everywhere it appeared.

The whole thing took an evening. Most of that was the editor rewrite, not the migration.

## What I'd take from this

**If your "structured" representation is already storing strings with conventions, it isn't structured.** It's a string with extra steps. Either commit to the string, or commit to making the structure load-bearing (validators, exhaustive types, no string fallback fields).

**Count the consumers, not the producers.** I was thinking about the editor (the producer) when I picked the schema. I should have been thinking about the eight or nine readers — agent tool, sharing, insights, auto-tag, search, list previews, exports — that all wanted the same thing the editor wasn't giving them.

**A "structured" schema you don't need is more lock-in than freedom.** It feels like you're keeping options open. You're actually adding a translation layer between you and every option.

The diff that matters isn't `+796 / −854`. It's that there is now exactly one canonical form of a note's body — a markdown string the user typed — and every layer of the stack reads from it directly. That's the kind of refactor that pays compounding interest, because every future feature that touches a note now starts from a place where the data is already in the form everything wants.
