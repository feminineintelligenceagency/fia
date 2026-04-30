<script lang="ts">
	import { Button } from '$lib/components/ui/button/index.js';
	import MoonIcon from '@lucide/svelte/icons/moon';
	import SunIcon from '@lucide/svelte/icons/sun';
	import { mode, toggleMode } from 'mode-watcher';
</script>

<Button onclick={toggleMode} size="icon-lg" class="rounded-full">
	{#if mode.current === 'dark'}
		<SunIcon />
	{:else}
		<MoonIcon />
	{/if}
</Button>
