<template>
  <div class="task-item">
    <div class="task-id">1</div>

    <div class="task-description">
      <button class="chapter-name" type="button">
        Trigonometry
      </button>
      <span class="title">Quiz 1</span>
    </div>

    <div class="task-status">
      10:00 min
    </div>

    <div class="task-priority">
      completed
    </div>

    <div class="task-actions">
      <button
        class="more-button"
        type="button"
        aria-label="More options"
      >
        <span class="dots"></span>
      </button>
    </div>
  </div>
</template>

<style scoped>
:root {
  --background: hsl(0 0% 100%);
  --foreground: hsl(222.2 84% 4.9%);
  --card: hsl(0 0% 100%);
  --card-foreground: hsl(222.2 84% 4.9%);
  --popover: hsl(0 0% 100%);
  --popover-foreground: hsl(222.2 84% 4.9%);
  --primary: hsl(222.2 47.4% 11.2%);
  --primary-foreground: hsl(210 40% 98%);
  --secondary: hsl(210 40% 96.1%);
  --secondary-foreground: hsl(222.2 47.4% 11.2%);
  --muted: hsl(210 40% 96.1%);
  --muted-foreground: hsl(215.4 16.3% 46.9%);
  --accent: hsl(210 40% 96.1%);
  --accent-foreground: hsl(222.2 47.4% 11.2%);
  --destructive: hsl(0 84.2% 60.2%);
  --destructive-foreground: hsl(210 40% 98%);
  --border: hsl(214.3 31.8% 91.4%);
  --input: hsl(214.3 31.8% 91.4%);
  --ring: hsl(222.2 84% 4.9%);
  --radius: 0.5rem;
}

.dark {
  --background: hsl(222.2 84% 4.9%);
  --foreground: hsl(210 40% 98%);
  --card: hsl(222.2 84% 4.9%);
  --card-foreground: hsl(210 40% 98%);
  --popover: hsl(222.2 84% 4.9%);
  --popover-foreground: hsl(210 40% 98%);
  --primary: hsl(210 40% 98%);
  --primary-foreground: hsl(222.2 47.4% 11.2%);
  --secondary: hsl(217.2 32.6% 17.5%);
  --secondary-foreground: hsl(210 40% 98%);
  --muted: hsl(217.2 32.6% 17.5%);
  --muted-foreground: hsl(215 20.2% 65.1%);
  --accent: hsl(217.2 32.6% 17.5%);
  --accent-foreground: hsl(210 40% 98%);
  --destructive: hsl(0 62.8% 30.6%);
  --destructive-foreground: hsl(210 40% 98%);
  --border: hsl(217.2 32.6% 17.5%);
  --input: hsl(217.2 32.6% 17.5%);
  --ring: hsl(212.7 26.8% 83.9%);
}

.task-item {
  display: flex;
  align-items: center;
  padding: 0.75rem 1rem;
  border-radius: var(--radius);
  border: 1px solid var(--border);
  background-color: var(--card);
  color: var(--card-foreground);
  transition: background-color 0.2s ease;
}

.task-item:hover {
  background-color: var(--muted);
}

.task-id {
  width: 2.5rem;
  text-align: center;
  color: var(--muted-foreground);
  font-weight: 300;
  margin-right: 1rem;
}

.task-description {
  flex: 1;
  display: flex;
  align-items: center;
  min-width: 0;
  overflow: hidden;
}

.chapter-name {
  font-size: 0.75rem;
  padding: 0.25rem 0.625rem;
  margin-right: 0.75rem;
  border-radius: calc(var(--radius) - 0.125rem);
  border: 1px solid var(--border);
  background-color: var(--background);
  color: var(--foreground);
  transition: background-color 0.2s ease;
}

.chapter-name:hover {
  background-color: var(--muted);
}

.title {
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  font-size: 0.875rem;
}

.task-status {
  margin: 0 1rem;
  padding: 0.25rem 0.75rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  background-color: var(--secondary);
  color: var(--secondary-foreground);
  min-width: 5rem;
  text-align: center;
}

.task-priority {
  min-width: 5rem;
  font-size: 0.875rem;
  color: var(--muted-foreground);
  text-transform: capitalize;
  margin-right: 1rem;
}

.task-actions {
  display: flex;
  align-items: center;
}

.more-button {
  display: flex;
  align-items: center;
  justify-content: center;
  width: 2rem;
  height: 2rem;
  padding: 0;
  border: none;
  background: transparent;
  border-radius: var(--radius);
  cursor: pointer;
  transition: background-color 0.2s ease;
}

.more-button:hover {
  background-color: var(--muted);
}

.more-button:focus {
  outline: none;
  box-shadow: 0 0 0 2px var(--background), 0 0 0 4px var(--ring);
}

.dots {
  position: relative;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background-color: var(--muted-foreground);
}

.dots::before,
.dots::after {
  content: "";
  position: absolute;
  width: 4px;
  height: 4px;
  border-radius: 50%;
  background-color: var(--muted-foreground);
}

.dots::before {
  top: -6px;
}

.dots::after {
  top: 6px;
}
</style>
