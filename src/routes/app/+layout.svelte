<script lang="ts">
	import { resolve } from '$app/paths';
	import { Button } from '$lib/components/ui/button/index.js';
	import Home from '@lucide/svelte/icons/house';
	import ScrollText from '@lucide/svelte/icons/scroll-text';

	const links = [
		{
			href: '/app',
			icon: Home
		},
		{
			href: '/app/posts',
			icon: ScrollText
		}
	];

	let { children } = $props();
</script>

<div class="flex h-full w-full">
	<div
		class="flex h-full w-24 flex-col items-center space-y-4 border-r border-slate-200/70 bg-white/70 p-4 backdrop-blur-xl"
	>
		<a href={resolve('/app')}>
			<img src="/logo.jpg" alt="FIA Logo" class="h-12 w-12 rounded-2xl object-cover shadow-sm" />
		</a>

		<div class="h-px w-10 bg-slate-200/80"></div>

		{#each links as link (link.href)}
			<Button
				size="icon-lg"
				variant="ghost"
				href={link.href}
				class="rounded-2xl border border-slate-200 bg-white shadow-sm hover:bg-slate-50"
			>
				<link.icon class="size-6 text-pink-300" />
			</Button>
		{/each}
	</div>

	<div class="flex h-full w-full flex-col overflow-x-hidden overflow-y-scroll p-4">
		{@render children()}
	</div>
</div>
