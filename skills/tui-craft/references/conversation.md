# Conversation and agent sessions

Use when communication is the primary task. Keep conversation navigation, transcript, and composer central. Secondary task lists, artifacts, approvals, and agent details support that flow; they must not displace it by default.

## Identity and causality

Keep stable conversation, participant, message, run, and parent/reference IDs. Render author/role words and destination/scope where needed, not color alone. Membership, message visibility, mention routing, wakeup, and execution are distinct concepts; implement the product's rules instead of assuming every member sees or runs everything.

Show assignments, questions, replies, relays, findings, handoffs, revisions, and completion where they belong. Link direct and group conversations or parent/child sessions when crossing scope, preserving draft, selection, and return context. A spinner or task badge cannot substitute for visible agent communication. Display explicit communicated content and concise progress—not invented private reasoning. Tool receipts should expand into relevant output/artifacts without losing their source message.

## Streaming and concurrent work

Keep input editable during a stream. Define send-while-busy policy (queue, steer, parallel run, or reject with draft retained) from requirements; do not universally force queuing or interruption. Distinguish accepted, queued, running, waiting for input/permission, failed, cancelled, and finished. Cancellation stops future work where possible; it does not imply rollback of completed effects. Late chunks/results must carry IDs/generations so they cannot contaminate a new run or another chat.

Coalesce updates and bound the amount rendered per frame. For inline history, finalize completed content once and update only the live region; for full-screen transcripts, use viewport rendering and stable scroll anchors. Neither requires rendering every historical turn on every token. Preserve code blocks and partial markup without exceptions while data is incomplete. Follow policy is in [interaction](interaction.md); urgent questions need a visible cue/link, not a forced scroll that destroys the reading position.

## Composer and action safety

Keep per-conversation drafts and cursor/scroll state. Grow a multiline composer to a reasonable cap, then scroll inside it; retain enough history and controls to understand the action. Bracketed paste never sends. Make recipients and editing/submission mode unambiguous. Test mouse Send and its keyboard equivalent against the same handler.

When the application needs approval, show the exact action and scope with explicit choices; never time out to acceptance. Prevent a newly appearing prompt from consuming characters already being typed as approval. Unrelated background work may continue without shifting the prompt or its targets. Do not make approval the default for routine UI actions.

## Representative acceptance journey

Open a conversation by click and key; send an edited/pasted message; see author and recipient scope; stream a reply while composing the next draft; scroll away without being pulled back; inspect a linked agent exchange/artifact and return; cancel or resolve an error without losing history; switch chats and recover the correct draft; resize and repeat. For multi-agent products include a question/reply and handoff/return chain, not only independent agents printing status lines. Use a labeled fake transport for prototypes, then test the actual transport before claiming integration.
