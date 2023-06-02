---
title: "CI REST API Documentation"
date: 2023-05-29T18:13:42-05:00
Description: "A walkthrough to publish API documentation for a REST API through github pages"
Tags: []
Categories: []
DisableComments: false
---

This blog post details how you can create professional REST API documentation that is published every time you update your project's repository by using an OpenAPI specification, Swagger UI, and GitHub Actions. By the end of the tutorial, you'll have a user friendly webpage that details your REST API. My example repository is hosted [here](https://github.com/beaudrychase/sunrise-sunset-api), and the generated documentation is hosted [here](https://beaudrychase.xyz/sunrise-sunset-api/). Before we dive in to the tutorial, I want to describe the technologies and why you might want to add this to your project.

## Technologies

As I said in the intro, this tutorial uses 3 technologies to create and publish the documentation:

- OpenAPI Specification
- Swagger UI
- Github Actions

I'll briefly describe each of them for those unfamiliar, before explaining how they all fit together.

### OpenAPI Specification

> [link to project website](https://www.openapis.org)

OpenAPI Specification (OAS) is a standard for describing the interface of a HTTP API. It is a structured representation of an API that tells a user everything they need to know about consuming it. Information like which endpoints are defined, what parameters they use, and what their response contains, are all defined in the OAS specification. As the API developer, you need to create the OAS specification file that describes your API. The file itself is either JSON or YAML, and unless the user has a thorough understanding of the specification, it will be hard for them to understand it.

So what can you do with the OAS file? Lots of things. OAS is a widely adopted standard and there are many powerful tools that use your OAS file as input and build things based on it. These tools can generate [user client libraries](https://swagger.io/tools/swagger-codegen/), [interactive examples](https://blog.postman.com/postman-supports-openapi-3-0/), or user friendly documentation. 

### Swagger UI

> [link to project website](https://swagger.io/tools/swagger-ui/)

This brings us to the next technology used in this tutorial, Swagger UI, which generates documentation based on OAS files. It takes in the OAS file and generates a static and interactive webpage documenting your API. 

### GitHub Actions

GitHub Actions is GitHub's platform for continuous integration and continuous development (CI/CD). With this platform you can run actions that are 


