<script lang="ts">
	import '../app.css';
	import { Toaster } from '$lib/components/ui/sonner/index.js';

	import { ModeWatcher } from 'mode-watcher';
	import ModeToggle from '$lib/components/ui/ModeToggle.svelte';

	let { children } = $props();
</script>

<ModeWatcher />

<!-- Global toggle (shows on every page) -->
<div class="fixed right-4 top-4 z-50">
	<ModeToggle />
</div>

<main class="h-full w-full overflow-hidden">
	{@render children()}
</main>

<Toaster richColors position="bottom-right" />
