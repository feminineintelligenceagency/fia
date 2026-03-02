<script lang="ts">
	import { toggleMode } from 'mode-watcher';
	import SunIcon from '@lucide/svelte/icons/sun';
	import MoonIcon from '@lucide/svelte/icons/moon';

	import { Button } from '$lib/components/ui/button/index.js';
</script>

<Button
	type="button"
	variant="outline"
	size="icon"
	onclick={toggleMode}
	class="relative rounded-full border border-slate-200 bg-white/70 backdrop-blur shadow-sm
	       hover:bg-slate-50
	       dark:border-slate-700 dark:bg-slate-900/60 dark:hover:bg-slate-900"
>
	<!-- Light mode -->
	<SunIcon class="h-4 w-4 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />

	<!-- Dark mode -->
	<MoonIcon class="absolute h-4 w-4 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />

	<span class="sr-only">Toggle theme</span>
</Button>