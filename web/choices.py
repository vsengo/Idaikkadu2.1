class choice:
        CATEGORY_CHOICES = (
            ('international', 'International'),
            ('srilanka', 'Sri Lanka'),
            ('jaffna', 'Jaffna'),
            ('idaikkadu', 'Idaikkadu'),
            ('australia', 'Australia'),
            ('canada', 'Canada'),
            ('swiss', 'Swiss'),
            ('uk', 'UK'),
            ('europe', 'Europe'),
            ('middleeast', 'Middle East'),
            ('asia', 'Asia'),
        )

        MENU_CHOICES = (
            ('News', 'News'),
            ('Obituary', 'Obituary'),
            ('Story', 'Story'),
            ('Association', 'Association'),
            ('Article', 'Articles'),
            ('Thankyou', 'Thankyou'),
            ('Temple', 'Temple'),
            ('Library', 'Library'),
            ('Wedding', 'Wedding'),
            ('Invitation', 'Invitation'),
            ('Other', 'Other'),
        )

        SECTION_CHOICES = (
            ('F', 'International'),
            ('I', 'Idaikkadu'),
            ('S', 'Srilanka'),
        )

        APPROVAL_CHOICES = (
            ('Y', 'Yes'),
            ('N', 'No'),
        )
