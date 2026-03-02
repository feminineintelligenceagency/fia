<script lang="ts">
	import { setContext, type Snippet } from 'svelte';

	let { children }: { children: Snippet } = $props();

	let id = $props.id();

	setContext('id', id);
</script>

<div class="space-y-2">
	{@render children()}
</div>
