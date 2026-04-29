<script lang="ts">
	import { invalidate } from '$app/navigation';
	import {
		ChatBubble,
		ChatBubbleAvatar,
		ChatBubbleMessage
	} from '$lib/components/ui/chat/chat-bubble/index.js';
	import { ChatInput, ChatMessageList } from '$lib/components/ui/chat/index.js';
	import { Button } from '$lib/components/ui/button/index.js';
	import { handleError } from '$lib/consts';
	import { sendChatMessage } from '$lib/data.remote';
	import ArrowUpIcon from '@lucide/svelte/icons/arrow-up';
	import ArrowLeftIcon from '@lucide/svelte/icons/arrow-left';

	let { data } = $props();

	let content = $state('');
	let sending = $state(false);

	let optimisticMessages = $state<
		{ id: number; role: 'user' | 'assistant'; content: string | null; isLoading?: boolean }[]
	>([]);

	async function send() {
		const text = content.trim();
		if (!text || sending) return;

		sending = true;
		content = '';

		const tempUserId = Date.now();
		const tempAiId = Date.now() + 1;

		optimisticMessages = [
			...optimisticMessages,
			{ id: tempUserId, role: 'user', content: text },
			{ id: tempAiId, role: 'assistant', content: null, isLoading: true }
		];

		try {
			const reply = await sendChatMessage({ chat_id: data.chat.id, content: text });

			optimisticMessages = optimisticMessages
				.filter((m) => m.id !== tempAiId)
				.map((m) => (m.id === tempUserId ? { ...m } : m));

			optimisticMessages = [
				...optimisticMessages,
				{ id: tempAiId, role: 'assistant', content: reply }
			];

			await invalidate('chat');
			optimisticMessages = [];
		} catch (err) {
			optimisticMessages = optimisticMessages.filter(
				(m) => m.id !== tempUserId && m.id !== tempAiId
			);
			handleError(err);
		} finally {
			sending = false;
		}
	}

	function onKeydown(e: KeyboardEvent) {
		if (e.key === 'Enter' && !e.shiftKey) {
			e.preventDefault();
			send();
		}
	}

	const allMessages = $derived([
		...data.messages.map((m) => ({ id: m.id, role: m.role, content: m.content, isLoading: false })),
		...optimisticMessages
	]);
</script>

<div class="flex h-full flex-col">
	<div
		class="flex items-center gap-3 border-b border-slate-200 bg-white/80 px-4 py-3 backdrop-blur"
	>
		<Button href="/app/chats" variant="ghost" size="icon" class="rounded-xl">
			<ArrowLeftIcon class="size-4" />
		</Button>
		<h1 class="truncate text-sm font-semibold text-slate-900">{data.chat.title}</h1>
	</div>

	<div class="flex-1 overflow-y-auto">
		<ChatMessageList>
			{#each allMessages as message (message.id)}
				<ChatBubble variant={message.role === 'user' ? 'sent' : 'received'}>
					<ChatBubbleAvatar fallback={message.role === 'user' ? 'Me' : 'AI'} />
					<ChatBubbleMessage
						variant={message.role === 'user' ? 'sent' : 'received'}
						isLoading={message.isLoading ?? false}
					>
						{message.content}
					</ChatBubbleMessage>
				</ChatBubble>
			{/each}
		</ChatMessageList>
	</div>

	<div class="sticky bottom-0 border-t border-slate-200 bg-white/80 p-4 backdrop-blur-md">
		<div class="flex gap-2">
			<ChatInput
				bind:value={content}
				placeholder="Type a message..."
				disabled={sending}
				onkeydown={onKeydown}
				class="flex-1"
			/>
			<Button
				onclick={send}
				disabled={sending || content.trim().length === 0}
				size="icon"
				class="mt-auto rounded-xl bg-pink-500 hover:bg-pink-500/90"
			>
				<ArrowUpIcon class="size-4" />
			</Button>
		</div>
	</div>
</div>
