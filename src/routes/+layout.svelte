<script lang="ts">
	import ModeToggle from '$lib/components/ModeToggle.svelte';
	import { Toaster } from '$lib/components/ui/sonner/index.js';
	import { ModeWatcher } from 'mode-watcher';
	import '../app.css';

	let { children } = $props();
</script>

<ModeWatcher />

<div class="pointer-events-auto fixed top-4 right-4 z-9999">
	<ModeToggle />
</div>

<main class="h-full w-full overflow-hidden">
	{@render children()}
</main>

<Toaster richColors position="bottom-right" />
