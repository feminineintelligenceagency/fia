<script lang="ts">
	import { goto } from '$app/navigation';
	import { resolve } from '$app/paths';
	import { Button } from '$lib/components/ui/button/index.js';
	import { handleError } from '$lib/consts';
	import { createChat } from '$lib/data.remote';
	import MessageCircleMoreIcon from '@lucide/svelte/icons/message-circle-more';
	import PlusIcon from '@lucide/svelte/icons/plus';

	let { data } = $props();

	let btnDisabled = $state(false);

	async function handleNewChat() {
		try {
			btnDisabled = true;
			const chat_id = await createChat();
			await goto(resolve('/app/chats/[chat_id]', { chat_id }));
		} catch (err) {
			handleError(err);
		} finally {
			btnDisabled = false;
		}
	}
</script>

<div class="mx-auto flex h-full w-full max-w-2xl flex-col gap-6 p-6">
	<div class="flex items-center justify-between">
		<h1 class="text-2xl font-bold text-slate-900">Chats</h1>
		<Button
			onclick={handleNewChat}
			disabled={btnDisabled}
			class="gap-2 rounded-xl bg-pink-500 hover:bg-pink-500/90"
		>
			<PlusIcon class="size-4" />
			New Chat
		</Button>
	</div>

	{#if data.chats.length === 0}
		<div
			class="flex flex-1 flex-col items-center justify-center gap-4 rounded-2xl border border-dashed border-slate-200 py-20 text-center"
		>
			<MessageCircleMoreIcon class="size-10 text-slate-300" />
			<p class="text-sm text-slate-500">No chats yet. Start a new one.</p>
			<Button
				onclick={handleNewChat}
				disabled={btnDisabled}
				size="sm"
				class="rounded-xl bg-pink-500 hover:bg-pink-500/90"
			>
				<PlusIcon class="size-4" />
				New Chat
			</Button>
		</div>
	{:else}
		<div class="flex flex-col gap-2">
			{#each data.chats as chat (chat.id)}
				<a
					href="/app/chats/{chat.id}"
					class="flex items-center gap-4 rounded-2xl border border-slate-200 bg-white px-4 py-4 transition hover:border-slate-300 hover:bg-slate-50 active:scale-[0.995]"
				>
					<div
						class="flex size-10 shrink-0 items-center justify-center rounded-xl bg-pink-50 text-pink-400"
					>
						<MessageCircleMoreIcon class="size-5" />
					</div>
					<div class="min-w-0 flex-1">
						<p class="truncate text-sm font-medium text-slate-900">{chat.title}</p>
						<p class="mt-0.5 text-xs text-slate-400">
							{chat.when_created
								? new Date(chat.when_created).toLocaleDateString(undefined, {
										month: 'short',
										day: 'numeric',
										year: 'numeric'
									})
								: ''}
						</p>
					</div>
				</a>
			{/each}
		</div>
	{/if}
</div>
