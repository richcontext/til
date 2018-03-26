class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = factory.Sequence(lambda n: 'username%s' % n)

class PublicationAPIActivityFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = PublicationAPIActivity

    publication = factory.SubFactory(PublicationFactory)
    retail_platform_page = factory.SubFactory(RetailPlatformPageFactory)


class TagFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Tag

    name = faker.lorem(words=5)

class ClientFactory(BaseModelFactory):
    class Meta:
        model = Client

    name = faker.company_name()

    @factory.post_generation
    def tags(self, create, extracted, **kwargs):
        if not create:
            return

        if extracted:
            for tag in extracted:
                self.tags.add(tag)
