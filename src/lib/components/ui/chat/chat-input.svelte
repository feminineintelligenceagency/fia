<script lang="ts">
	import type { WithElementRef } from 'bits-ui';
	import type { HTMLTextareaAttributes } from 'svelte/elements';
	import { Textarea } from '../textarea/index.js';

	type ChatInputProps = WithElementRef<HTMLTextareaAttributes>;

	let {
		class: className,
		ref = $bindable(null),
		value = $bindable(),
		...restProps
	}: ChatInputProps = $props();
</script>

<Textarea
	bind:value
	autocomplete="off"
	{ref}
	name="message"
	class={[
		'flex max-h-48 w-full items-center rounded-md bg-background px-4 py-3 text-sm placeholder:text-muted-foreground focus-visible:ring-ring focus-visible:outline-none disabled:cursor-not-allowed disabled:opacity-50',
		className
	]}
	{...restProps}
/>
