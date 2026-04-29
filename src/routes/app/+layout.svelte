<script lang="ts">
	import { resolve } from '$app/paths';
	import { Button } from '$lib/components/ui/button/index.js';
	import Brain from '@lucide/svelte/icons/brain';
	import Activity from '@lucide/svelte/icons/activity';
	import Home from '@lucide/svelte/icons/house';
	import Chat from '@lucide/svelte/icons/message-circle-more';
	import ScrollText from '@lucide/svelte/icons/scroll-text';
	import FileUp from '@lucide/svelte/icons/file-up';

	const links = [
		{
			href: '/app',
			icon: Home
		},
		{
			href: '/app/posts',
			icon: ScrollText
		},
		{
			href: '/app/rag',
			icon: Brain
			href: '/app/scenario-analyzer',
			icon: Activity
		},
		{
			href: '/app/chats',
			icon: Chat
		},
		{
			href: '/app/script-upload-analyzer',
			icon: FileUp
		}
	];

	let { children } = $props();
</script>

<div class="flex h-full w-full">
	<!-- Sidebar -->
	<div
		class="flex h-full w-24 flex-col items-center space-y-4 border-r border-slate-700/40 bg-slate-950/40 p-4 backdrop-blur-xl"
	>
		<a href={resolve('/app')}>
			<img src="/logo.jpg" alt="FIA Logo" class="h-12 w-12 rounded-2xl object-cover shadow-sm" />
		</a>

		<div class="h-px w-10 bg-slate-700/40"></div>

		{#each links as link (link.href)}
			<Button
				size="icon-lg"
				variant="ghost"
				href={link.href}
				class="rounded-2xl border border-slate-700/40 bg-slate-950/30 shadow-sm hover:bg-slate-900/40"
			>
				<link.icon class="size-6 text-pink-300" />
			</Button>
		{/each}
	</div>

	<!-- Content -->
	<div class="flex h-full w-full flex-col overflow-x-hidden overflow-y-scroll p-4">
		{@render children()}
	</div>
</div>