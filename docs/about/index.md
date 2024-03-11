---
title: About
draft: false 
date: 2024-03-01
authors:
  - grumpydumpty
hide:
  - navigation
  - toc
---

# Structure of this site

```mermaid
graph TD
    A(euc.github.io)
    A --> B(Products)
    A --> C(Architecture)
    A --> D(APIs)
    A --> E(PowerCLI)
    A --> F(Code Samples)
    A --> G(SDKs)
    A --> H("{code}")
```

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque nec maximus ex. Sed consequat, nulla quis malesuada dapibus, elit metus vehicula erat, ut egestas tellus eros at risus. In hac habitasse platea dictumst. Phasellus id lacus pulvinar erat consequat pretium. Morbi malesuada arcu mauris Nam vel justo sem. Nam placerat purus non varius luctus. Integer pretium leo in sem rhoncus, quis gravida orci mollis. Proin id aliquam est. Vivamus in nunc ac metus tristique pellentesque. Suspendisse viverra urna in accumsan aliquet.

## Alternative Approach

Donec volutpat, elit ac volutpat laoreet, turpis dolor semper nibh, et dictum massa ex pulvinar elit. Curabitur commodo sit amet dolor sed mattis. Etiam tempor odio eu nisi gravida cursus. Maecenas ante enim, fermentum sit amet molestie nec, mollis ac libero. Vivamus sagittis suscipit eros ut luctus.

```mermaid
graph TD
    A(euc.github.io)
    A --> B(/products)
    A --> C(/developer)
    A --> D(/blogs)
    A --> E(. . .)
```

Nunc vehicula sagittis condimentum. Cras facilisis bibendum lorem et feugiat. In auctor accumsan ligula, at consectetur erat commodo quis. Morbi ac nunc pharetra, pellentesque risus in, consectetur urna. Nulla id enim facilisis arcu tincidunt pulvinar. Vestibulum laoreet risus scelerisque porta congue. In velit purus, dictum quis neque nec, molestie viverra risus. Nam pellentesque tellus id elit ultricies, vel finibus erat cursus.

```mermaid
graph TD
    B(/products)
    B --> F(UEM)
    B --> G(Horizon)
    B --> H(Workspace ONE)
    B --> I(. . .)
```

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque nec maximus ex. Sed consequat, nulla quis malesuada dapibus, elit metus vehicula erat, ut egestas tellus eros at risus. In hac habitasse platea dictumst. Phasellus id lacus pulvinar erat consequat pretium. Morbi malesuada arcu mauris Nam vel justo sem. Nam placerat purus non varius luctus. Integer pretium leo in sem rhoncus, quis gravida orci mollis. Proin id aliquam est. Vivamus in nunc ac metus tristique pellentesque. Suspendisse viverra urna in accumsan aliquet.

The developer section could be structured by product e.g.:

```mermaid
graph TD
    C(/developer)
    C --> I(UEM)
    C --> J(Horizon)
    C --> K(Workspace ONE)
    C --> L(PowerCLI)
    C --> M(. . .)
```

Alternatively, you could do function-based structure e.g.:

```mermaid
graph TD
    C(/developer)
    C --> D(SDKs)
    C --> E(APIs)
    C --> F(PowerCLI)
    C --> G(Samples)
    D --> I(UEM)
    D --> J(Horizon)
    D --> K(Workspace ONE)
    D --> M(. . .)
    E --> N(UEM)
    E --> O(Horizon)
    E --> P(Workspace ONE)
    E --> Q(. . .)
    F --> R(UEM)
    F --> S(Horizon)
    F --> T(Workspace ONE)
    F --> U(. . .)
    G --> V(UEM)
    G --> W(Horizon)
    G --> X(Workspace ONE)
    G --> Y(. . .)
```


Donec volutpat, elit ac volutpat laoreet, turpis dolor semper nibh, et dictum massa ex pulvinar elit. Curabitur commodo sit amet dolor sed mattis. Etiam tempor odio eu nisi gravida cursus. Maecenas ante enim, fermentum sit amet molestie nec, mollis ac libero. Vivamus sagittis suscipit eros ut luctus.

The blogs section could be structured by product e.g.:

```mermaid
graph TD
    D(/blogs)
    D --> M(UEM)
    D --> N(Horizon)
    D --> O(Workspace ONE)
    D --> P(PowerCLI)
    D --> Q(. . .)
```

Though you are more likely to use `tags` and `categories` to group and filter the blogs posts.

Nunc vehicula sagittis condimentum. Cras facilisis bibendum lorem et feugiat. In auctor accumsan ligula, at consectetur erat commodo quis. Morbi ac nunc pharetra, pellentesque risus in, consectetur urna. Nulla id enim facilisis arcu tincidunt pulvinar. Vestibulum laoreet risus scelerisque porta congue. In velit purus, dictum quis neque nec, molestie viverra risus. Nam pellentesque tellus id elit ultricies, vel finibus erat cursus.

Everything in in a single diagram:

```mermaid
graph TD
    A(euc.github.io)
    A --> B(/products)
    A --> C(/developer)
    A --> D(/blogs)
    A --> E(. . .)
    B --> F(UEM)
    B --> G(Horizon)
    B --> H(Workspace ONE)
    C --> I(UEM)
    C --> J(Horizon)
    C --> K(Workspace ONE)
    C --> L(PowerCLI)
    D --> M(UEM)
    D --> N(Horizon)
    D --> O(Workspace ONE)
    D --> P(PowerCLI)
    E --> R(. . .)
    E --> S(. . .)
```

Lorem ipsum dolor sit amet, consectetur adipiscing elit. Pellentesque nec maximus ex. Sed consequat, nulla quis malesuada dapibus, elit metus vehicula erat, ut egestas tellus eros at risus. In hac habitasse platea dictumst. Phasellus id lacus pulvinar erat consequat pretium. Morbi malesuada arcu mauris Nam vel justo sem. Nam placerat purus non varius luctus. Integer pretium leo in sem rhoncus, quis gravida orci mollis. Proin id aliquam est. Vivamus in nunc ac metus tristique pellentesque. Suspendisse viverra urna in accumsan aliquet.
