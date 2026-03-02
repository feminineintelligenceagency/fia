<script lang="ts">
	import ModeToggle from '$lib/components/ModeToggle.svelte';
	import { Toaster } from '$lib/components/ui/sonner/index.js';
	import '../app.css';

	let { children } = $props();
</script>

<!-- Global toggle (shows on every page) -->
<div class="fixed top-4 right-4 z-50">
	<ModeToggle />
</div>

<main class="h-full w-full overflow-hidden">
	{@render children()}
</main>

<Toaster richColors position="bottom-right" />
