<script lang="ts">
	import { onMount } from 'svelte';
	import SunIcon from '@lucide/svelte/icons/sun';
	import MoonIcon from '@lucide/svelte/icons/moon';

	let isDark = false;

	function apply(dark: boolean) {
		isDark = dark;
		document.documentElement.classList.toggle('dark', dark);
		localStorage.setItem('theme', dark ? 'dark' : 'light');
	}

	onMount(() => {
		const saved = localStorage.getItem('theme');
		if (saved === 'dark' || saved === 'light') apply(saved === 'dark');
		else apply(window.matchMedia('(prefers-color-scheme: dark)').matches);
	});

	function toggle() {
		apply(!isDark);
	}
</script>

<button
	type="button"
	on:click={toggle}
	aria-label="Toggle theme"
	class="relative inline-flex h-10 w-10 items-center justify-center rounded-full
	       border border-slate-700/40 bg-slate-950/30 text-slate-100
	       backdrop-blur shadow-sm hover:bg-slate-900/40"
>
	<!-- Light mode icon -->
	<SunIcon class="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />

	<!-- Dark mode icon -->
	<MoonIcon class="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
</button>