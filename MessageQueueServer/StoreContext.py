class StoreContext:
    def __init__(self):
        self.subjectStore = dict({
            "SpringBoot": """Spring Boot makes it easy to create stand-alone, production-grade Spring based Applications that \nyou can "just run". We take an opinionated view of the Spring platform and third-party libraries so you can get started with minimum fuss.\nMost Spring Boot applications need minimal Spring configuration.""",
            "NodeJs": """Node.js® is a free, open-source,\ncross-platform JavaScript runtime environment that lets developers create servers, web apps,\ncommand line tools and scripts.""",
            "React": """React The library for web and native user interfaces.\nReact lets you build user interfaces out of individual pieces called components.""",
            "Django": """Django is a high-level Python web framework that encourages rapid development and clean, pragmatic design. Built by experienced developers,\nit takes care of much of the hassle of web development, so you can focus on writing your app without needing to reinvent the wheel.\nIt’s free and open source."""
        })
        self.emailStore = dict({
            "SpringBoot": [],
            "NodeJs": [],
            "React": [],
            "Django": [],
        })

    def isExistSubject(self, user_subject):
        if user_subject in self.subjectStore:
            return True
        else:
            return False

    def deleteEmail(self,subject,email):
        self.emailStore[subject].remove(email)
        print(f"Email '{email}' has been removed from '{subject}' subject.")

    def getAllSubjectList(self):
        return list(self.subjectStore.keys())

    def getContentBySubject(self,subject):
        return self.subjectStore[subject]

    def addContentSubjectStore(self, subject, newContent):
        if subject in self.subjectStore:
            self.subjectStore[subject] += f"\n{newContent}"
            return self.subjectStore[subject]
        else:
            print(f"Subject '{subject}' does not exist in subjectStore.")

    def getEmailStore(self, subject):
        return self.emailStore.get(subject,[])

    def addEmailBySubject(self, subject, email):
        if subject in self.emailStore:
            self.emailStore[subject].append(email)
            return self.subjectStore[subject]
        else:
            print(f"Subject '{subject}' does not exist in emailStore.")